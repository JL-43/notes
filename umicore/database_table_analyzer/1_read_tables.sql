USE PMR_HOB_PIFD_PRD

--------------------------------------------------------------------------------
-- Script: Sample 5 non-null values per column for every table in the database
--------------------------------------------------------------------------------
SET NOCOUNT ON;

DECLARE 
    @schemaName SYSNAME,
    @tableName  SYSNAME,
    @columnName SYSNAME,
    @sql        NVARCHAR(MAX);

--------------------------------------------------------------------------------
-- Cursor #1: Iterate over each user table in the database
--------------------------------------------------------------------------------
DECLARE table_cursor CURSOR FOR
    SELECT 
        s.name AS schemaName,
        t.name AS tableName
    FROM sys.tables t
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
	WHERE t.name LIKE '%AF%' 
    ORDER BY s.name, t.name;

OPEN table_cursor;
FETCH NEXT FROM table_cursor INTO @schemaName, @tableName;

WHILE @@FETCH_STATUS = 0
BEGIN
    -- PRINT 'Reading table: ' + @schemaName + '.' + @tableName;

    --------------------------------------------------------------------------------
    -- Cursor #2: Iterate over each column in the current table
    --------------------------------------------------------------------------------
    DECLARE column_cursor CURSOR FOR
        SELECT c.name
        FROM sys.columns c
        WHERE c.object_id = OBJECT_ID(@schemaName + '.' + @tableName)
        ORDER BY c.column_id;

    OPEN column_cursor;
    FETCH NEXT FROM column_cursor INTO @columnName;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Build dynamic query to read up to 5 non-null values for each column
        SET @sql = N'
            SELECT TOP 5
                  ''' + @schemaName + '.' + @tableName + ''' AS TableName
                , ''' + @columnName + ''' AS ColumnName
                , T.[' + @columnName + N'] AS SampleValue
                , C.DATA_TYPE       AS DataType
            FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N' AS T
            CROSS APPLY
            (
                SELECT DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = ''' + @schemaName + N'''
                  AND TABLE_NAME = ''' + @tableName + N'''
                  AND COLUMN_NAME = ''' + @columnName + N'''
            ) AS C
            WHERE T.[' + @columnName + N'] IS NOT NULL;
        ';

        -- Execute the dynamic query
        EXEC sp_executesql @sql;

        FETCH NEXT FROM column_cursor INTO @columnName;
    END;

    CLOSE column_cursor;
    DEALLOCATE column_cursor;

    FETCH NEXT FROM table_cursor INTO @schemaName, @tableName;
END;

CLOSE table_cursor;
DEALLOCATE table_cursor;

SET NOCOUNT OFF;
