# Database Table Analyzer

## TODO:

i have the following files

everything that does not have the 'new_' prefix in their file name is a working version of these files

new_1_read_tables.sql is a sql script that pulls data, similar to its counterpart that does not have 'new_' on it

the only difference between the two is that there is now a "data type" added in the results that it produces

that is also reflected in source.tsv and new_source.tsv as these are the outputs of this sql script, matching with their partners with the addition or lack 'new_' prefix

we want to edit the working code to incorporate this new change

currently, the "table.html" which acts as the final "report" renders the sample data tables like so

Sample Data
Filter TableName
 TableName	
Filter ColumnName
 ColumnName	
Filter MaxValue
 MaxValue	
Filter MinValue
 MinValue	
Filter AvgValue
 AvgValue	
Filter CountValue
 CountValue	
Filter DistinctCountValue
 DistinctCountValue	
Filter MaxDecimalPoints
 MaxDecimalPoints	
Filter MaxLength
 MaxLength	
Filter MinLength
 MinLength
dbo.AFEnumerationValue	id	NULL	NULL	NULL	1000	1000	NULL	NULL	NULL
dbo.AFEnumerationValue	rowversion	NULL	NULL	NULL	1000	1000	NULL	NULL	NULL
dbo.AFEnumerationValue	fkenumerationid	NULL	NULL	NULL	1000	62	NULL	NULL	NULL
dbo.AFEnumerationValue	name	NULL	NULL	NULL	1000	843	NULL	252	1
dbo.AFEnumerationValue	description	NULL	NULL	NULL	148	15	NULL	32	0
dbo.AFEnumerationValue	value	21426	0	2466.672	1000	421	NULL	NULL	NULL
dbo.AFEnumerationValue	changedby	196	0	37.006	1000	6	NULL	NULL	NULL

as you can see, it only includes the informational details about the columns but not the actual sample data (which is basically a head(5))

it also does not have the data types of each column

for the sample table i provided, let's add the data type

and for the head(5) let's render a completely new table below it that shows this sample data

these are the most important instructions:

you are not to code these, instead, you are to look at these instructions and prepare a more clear version of my instructions to feed into another LLM agent

## Objective:
Update the existing code to incorporate the new changes from `new_1_read_tables.sql` and `new_source.tsv`. The changes include adding the "data type" to the results and rendering sample data in the final report.

## Instructions:

### 1. Update SQL Script:
- Ensure that `new_1_read_tables.sql` includes the "data type" in the results.
- Verify that the output of `new_1_read_tables.sql` matches the format of `new_source.tsv`.

### 2. Update Data Loading in `2_table_visualizer.py`:
- Modify the `load_data` function to handle the new "data type" column in `new_source.tsv`.
- Ensure that both `column_info_df` and `sample_value_df` DataFrames correctly parse and include the "data type" column.

### 3. Update HTML Templates:
#### `table.html`:
- **Add Data Type Column**:
  - Update the table that displays column information to include the "data type" for each column.
  - Ensure that the "data type" is displayed alongside other column details like MaxValue, MinValue, etc.
- **Render Sample Data**:
  - Create a new table below the existing column information table to display the sample data (head(5)).
  - Ensure that this new table includes the sample values for each column.

### 4. Example of Updated HTML Structure:
#### Column Information Table:
\`\`\`html
<table class="min-w-full divide-y divide-gray-200 table-auto">
    <thead class="bg-gray-100">
        <tr>
            <th>TableName</th>
            <th>ColumnName</th>
            <th>DataType</th>
            <th>MaxValue</th>
            <th>MinValue</th>
            <th>AvgValue</th>
            <th>CountValue</th>
            <th>DistinctCountValue</th>
            <th>MaxDecimalPoints</th>
            <th>MaxLength</th>
            <th>MinLength</th>
        </tr>
    </thead>
    <tbody>
        <!-- Dynamically render rows -->
        {% for row in table_data %}
        <tr>
            <td>{{ row.TableName }}</td>
            <td>{{ row.ColumnName }}</td>
            <td>{{ row.DataType }}</td>
            <td>{{ row.MaxValue }}</td>
            <td>{{ row.MinValue }}</td>
            <td>{{ row.AvgValue }}</td>
            <td>{{ row.CountValue }}</td>
            <td>{{ row.DistinctCountValue }}</td>
            <td>{{ row.MaxDecimalPoints }}</td>
            <td>{{ row.MaxLength }}</td>
            <td>{{ row.MinLength }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
\`\`\`

#### Sample Data Table:
\`\`\`html
<h3 class="text-xl font-semibold mb-2">Sample Data</h3>
<table class="min-w-full divide-y divide-gray-200 table-auto">
    <thead class="bg-gray-100">
        <tr>
            <th>TableName</th>
            <th>ColumnName</th>
            <th>DataType</th>
            <th>SampleValue</th>
        </tr>
    </thead>
    <tbody>
        <!-- Dynamically render rows -->
        {% for row in sample_data %}
        <tr>
            <td>{{ row.TableName }}</td>
            <td>{{ row.ColumnName }}</td>
            <td>{{ row.DataType }}</td>
            <td>{{ row.SampleValue }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
\`\`\`

### 5. Update Flask Routes:
- Ensure that the `/table/<table_name>` route in `2_table_visualizer.py` correctly passes the updated `table_data` and `sample_data` to the `table.html` template.

### 6. Testing:
- Verify that the updated `table.html` correctly displays the column information with data types and the sample data table.
- Ensure that the application correctly handles the new format of `new_source.tsv`.