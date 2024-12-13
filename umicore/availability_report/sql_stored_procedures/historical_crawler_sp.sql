use mock_target_server;
go

create or alter procedure dbo.migrate_historical_data
    @source_database varchar(255),
    @source_table varchar(255),
    @date_column varchar(255),
    @target_database varchar(255),
    @target_table varchar(255),
    @days_per_batch int = 3,
    @start_date datetime = null,
    @end_date datetime = '2016-01-01',
    @force_reprocess bit = 0
as
begin
    set nocount on;
    set xact_abort on;

    declare @batch_id uniqueidentifier = newid();
    declare @current_date datetime;
    declare @sql nvarchar(max);
    declare @params nvarchar(max);
    declare @error_message nvarchar(4000);
    declare @rows_affected int;

    -- Parameter validation
    if @days_per_batch <= 0
    begin
        raiserror('Days per batch must be greater than 0', 16, 1);
        return;
    end

    -- Get latest date if not specified
    if @start_date is null
    begin
        set @sql = N'
            select @start_date = max(' + quotename(@date_column) + ')
            from ' + quotename(@source_database) + '.' + quotename('dbo') + '.' + quotename(@source_table);
        
        set @params = N'@start_date datetime output';
        
        begin try
            exec sp_executesql @sql, @params, @start_date output;
        end try
        begin catch
            set @error_message = error_message();
            raiserror('Failed to get start date: %s', 16, 1, @error_message);
            return;
        end catch
    end

    set @current_date = @start_date;

    while @current_date >= @end_date
    begin
        declare @batch_start datetime = dateadd(day, -@days_per_batch + 1, @current_date);
        declare @batch_end datetime = @current_date;

        -- Handle reprocessing
        if @force_reprocess = 1
        begin
            -- Mark existing records for reprocess
            update dbo.data_migration_audit
            set execution_status = 'Reprocess'
            where start_date = @batch_start 
            and end_date = @batch_end
            and execution_status = 'Completed';

            -- Clean existing data from target
            set @sql = N'
                delete from ' + quotename(@target_database) + '.dbo.' + quotename(@target_table) + '
                where cast(' + quotename(@date_column) + ' as date) >= @batch_start
                and cast(' + quotename(@date_column) + ' as date) <= @batch_end';

            begin try
                exec sp_executesql @sql, N'@batch_start datetime, @batch_end datetime', 
                    @batch_start, @batch_end;
            end try
            begin catch
                set @error_message = error_message();
                raiserror('Failed to clean existing data: %s', 10, 1, @error_message);
                -- Continue processing
            end catch
        end

        -- Process if new or reprocessing
        if @force_reprocess = 1 
        or not exists (
            select 1 
            from dbo.data_migration_audit 
            where start_date = @batch_start 
            and end_date = @batch_end
            and execution_status = 'Completed'
        )
        begin
            set @sql = N'
                insert into ' + quotename(@target_database) + '.dbo.' + quotename(@target_table) + '
                select *
                from ' + quotename(@source_database) + '.dbo.' + quotename(@source_table) + '
                where cast(' + quotename(@date_column) + ' as date) >= @batch_start
                and cast(' + quotename(@date_column) + ' as date) <= @batch_end';

            insert into dbo.data_migration_audit (
                batch_id, source_database, source_table, target_database, target_table,
                date_column, start_date, end_date, execution_status, sql_command
            )
            values (
                @batch_id, @source_database, @source_table, @target_database, @target_table,
                @date_column, @batch_start, @batch_end, 'Started', @sql
            );

            begin try
                begin transaction;

                exec sp_executesql @sql, N'@batch_start datetime, @batch_end datetime',
                    @batch_start, @batch_end;
                
                set @rows_affected = @@rowcount;

                update dbo.data_migration_audit
                set execution_status = 'Completed',
                    rows_processed = @rows_affected,
                    end_time = getdate()
                where batch_id = @batch_id
                and start_date = @batch_start
                and end_date = @batch_end;

                commit transaction;
            end try
            begin catch
                if @@trancount > 0
                    rollback transaction;

                set @error_message = error_message();

                update dbo.data_migration_audit
                set execution_status = 'Failed',
                    error_message = @error_message,
                    end_time = getdate()
                where batch_id = @batch_id
                and start_date = @batch_start
                and end_date = @batch_end;

                raiserror('Failed to process batch %s to %s: %s', 10, 1,
                    convert(varchar, @batch_start, 120),
                    convert(varchar, @batch_end, 120),
                    @error_message);
            end catch
        end

        set @current_date = dateadd(day, -@days_per_batch, @current_date);
    end
end;
go