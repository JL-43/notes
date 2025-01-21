USE PMR_HOB_PIFD_PRD

--------------------------------------------------------------------------------
-- Script: Sample 5 non-null values per column for every table in the database
--------------------------------------------------------------------------------
SET NOCOUNT ON;

DECLARE 
    @schemaName SYSNAME,
    @tableName  SYSNAME,
    @columnName SYSNAME,
    @dataType   NVARCHAR(128),
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
        SELECT c.name, t.name AS dataType
        FROM sys.columns c
        JOIN sys.types t ON c.user_type_id = t.user_type_id
        WHERE c.object_id = OBJECT_ID(@schemaName + '.' + @tableName)
        ORDER BY c.column_id;

    OPEN column_cursor;
    FETCH NEXT FROM column_cursor INTO @columnName, @dataType;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        IF @dataType IN ('int', 'smallint', 'tinyint')
        BEGIN
            SET @sql = N'
                SELECT 
                      ''' + @schemaName + '.' + @tableName + ''' AS TableName
                    , ''' + @columnName + ''' AS ColumnName
                    , MAX(T.[' + @columnName + N']) AS MaxValue
                    , MIN(T.[' + @columnName + N']) AS MinValue
                    , AVG(CAST(T.[' + @columnName + N'] AS FLOAT)) AS AvgValue
                    , COUNT(T.[' + @columnName + N']) AS CountValue
                    , COUNT(DISTINCT T.[' + @columnName + N']) AS DistinctCountValue
                    , NULL AS MaxDecimalPoints
                    , NULL AS MaxLength
                    , NULL AS MinLength
                FROM (SELECT TOP 1000 * FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N') AS T
                WHERE T.[' + @columnName + N'] IS NOT NULL;

                SELECT TOP 5
                      ''' + @schemaName + '.' + @tableName + ''' AS TableName
                    , ''' + @columnName + ''' AS ColumnName
                    , T.[' + @columnName + N'] AS SampleValue
                FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N' AS T
                WHERE T.[' + @columnName + N'] IS NOT NULL;
            ';
        END
        ELSE IF @dataType IN ('bigint')
        BEGIN
            SET @sql = N'
                SELECT 
                      ''' + @schemaName + '.' + @tableName + ''' AS TableName
                    , ''' + @columnName + ''' AS ColumnName
                    , MAX(CAST(T.[' + @columnName + N'] AS FLOAT)) AS MaxValue
                    , MIN(CAST(T.[' + @columnName + N'] AS FLOAT)) AS MinValue
                    , AVG(CAST(T.[' + @columnName + N'] AS FLOAT)) AS AvgValue
                    , COUNT(T.[' + @columnName + N']) AS CountValue
                    , COUNT(DISTINCT T.[' + @columnName + N']) AS DistinctCountValue
                    , NULL AS MaxDecimalPoints
                    , NULL AS MaxLength
                    , NULL AS MinLength
                FROM (SELECT TOP 1000 * FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N') AS T
                WHERE T.[' + @columnName + N'] IS NOT NULL;

                SELECT TOP 5
                      ''' + @schemaName + '.' + @tableName + ''' AS TableName
                    , ''' + @columnName + ''' AS ColumnName
                    , T.[' + @columnName + N'] AS SampleValue
                FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N' AS T
                WHERE T.[' + @columnName + N'] IS NOT NULL;
            ';
        END
        ELSE IF @dataType IN ('decimal', 'numeric', 'float', 'real')
        BEGIN
            SET @sql = N'
                SELECT 
                      ''' + @schemaName + '.' + @tableName + ''' AS TableName
                    , ''' + @columnName + ''' AS ColumnName
                    , MAX(T.[' + @columnName + N']) AS MaxValue
                    , MIN(T.[' + @columnName + N']) AS MinValue
                    , AVG(T.[' + @columnName + N']) AS AvgValue
                    , COUNT(T.[' + @columnName + N']) AS CountValue
                    , COUNT(DISTINCT T.[' + @columnName + N']) AS DistinctCountValue
                    , MAX(LEN(CAST(T.[' + @columnName + N'] AS VARCHAR)) - CHARINDEX(''.'', CAST(T.[' + @columnName + N'] AS VARCHAR))) AS MaxDecimalPoints
                    , NULL AS MaxLength
                    , NULL AS MinLength
                FROM (SELECT TOP 1000 * FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N') AS T
                WHERE T.[' + @columnName + N'] IS NOT NULL;

                SELECT TOP 5
                      ''' + @schemaName + '.' + @tableName + ''' AS TableName
                    , ''' + @columnName + ''' AS ColumnName
                    , T.[' + @columnName + N'] AS SampleValue
                FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N' AS T
                WHERE T.[' + @columnName + N'] IS NOT NULL;
            ';
        END
        ELSE IF @dataType IN ('char', 'varchar', 'nchar', 'nvarchar', 'text', 'ntext')
        BEGIN
            SET @sql = N'
                SELECT 
                      ''' + @schemaName + '.' + @tableName + ''' AS TableName
                    , ''' + @columnName + ''' AS ColumnName
                    , NULL AS MaxValue
                    , NULL AS MinValue
                    , NULL AS AvgValue
                    , COUNT(T.[' + @columnName + N']) AS CountValue
                    , COUNT(DISTINCT T.[' + @columnName + N']) AS DistinctCountValue
                    , NULL AS MaxDecimalPoints
                    , MAX(LEN(T.[' + @columnName + N'])) AS MaxLength
                    , MIN(LEN(T.[' + @columnName + N'])) AS MinLength
                FROM (SELECT TOP 1000 * FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N') AS T
                WHERE T.[' + @columnName + N'] IS NOT NULL;

                SELECT TOP 5
                      ''' + @schemaName + '.' + @tableName + ''' AS TableName
                    , ''' + @columnName + ''' AS ColumnName
                    , T.[' + @columnName + N'] AS SampleValue
                FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N' AS T
                WHERE T.[' + @columnName + N'] IS NOT NULL;
            ';
        END
        ELSE
        BEGIN
            SET @sql = N'
                SELECT 
                      ''' + @schemaName + '.' + @tableName + ''' AS TableName
                    , ''' + @columnName + ''' AS ColumnName
                    , NULL AS MaxValue
                    , NULL AS MinValue
                    , NULL AS AvgValue
                    , COUNT(T.[' + @columnName + N']) AS CountValue
                    , COUNT(DISTINCT T.[' + @columnName + N']) AS DistinctCountValue
                    , NULL AS MaxDecimalPoints
                    , NULL AS MaxLength
                    , NULL AS MinLength
                FROM (SELECT TOP 1000 * FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N') AS T
                WHERE T.[' + @columnName + N'] IS NOT NULL;

                SELECT TOP 5
                      ''' + @schemaName + '.' + @tableName + ''' AS TableName
                    , ''' + @columnName + ''' AS ColumnName
                    , T.[' + @columnName + N'] AS SampleValue
                FROM ' + QUOTENAME(@schemaName) + N'.' + QUOTENAME(@tableName) + N' AS T
                WHERE T.[' + @columnName + N'] IS NOT NULL;
            ';
        END

        -- Execute the dynamic query
        EXEC sp_executesql @sql;

        FETCH NEXT FROM column_cursor INTO @columnName, @dataType;
    END;

    CLOSE column_cursor;
    DEALLOCATE column_cursor;

    FETCH NEXT FROM table_cursor INTO @schemaName, @tableName;
END;

CLOSE table_cursor;
DEALLOCATE table_cursor;

SET NOCOUNT OFF;
