# PI SDP API

## Initial Message

I am extracting data from Aveva PI.

Currently, we are exploring the option of extracting the data through a SQL Server extract with ADF--but architecturally, there are quite a lot of challenges.

To reduce dependency on the work of the architect and network team, I want to leverage the PI Web API which is already an available option for me to use.

For the moment, I have defined the data and schema that we need in a document.

The most important "facts" are from a table called "EventFrameSnapshot" (to start with).

The schema from SQL is not the same as the schema from the APIs (perhaps it is to do with the nature of it being JSON objects? unsure).

But, either way, this is a list of all the columns we need:

| Source Table/s                    | Source Column Name     | DWH Table Name      | DWH Column Name              | Data Type | IsNullable? | Remark / Logic                                                                                     |
|----------------------------------|------------------------|---------------------|------------------------------|----------|------------|------------------------------------------------------------------------------------------------------|
| [HOB].[Data].[EventFrameSnapshot] | EventFrameAttributeID  | EventFrameSnapshot  | eventframe_attribute_id      | Guid     | n          | lowest granularity fact id                                                                           |
| [HOB].[Data].[EventFrameSnapshot] | Time                   | EventFrameSnapshot  | time                         | DateTime | n          |                                                                                                      |
| [HOB].[Data].[EventFrameSnapshot] | Value                  | EventFrameSnapshot  | value                        | String   | y          |                                                                                                      |
| [HOB].[Data].[EventFrameSnapshot] | ValueGuid              | EventFrameSnapshot  | value_guid                   | Guid     | y          | equivalent to "enumerationid" in enumerationvalue table (out of 2979, 26 unique (including null))    |
| [HOB].[EventFrame].[EventFrame]   | ID                     | EventFrameSnapshot  | eventframe_id               | Guid     | n          | foreign key                                                                                          |
| [HOB].[EventFrame].[EventFrame]   | Name                   | EventFrameSnapshot  | eventframe_name             | String   | n          | 36 unique values                                                                                     |
| [HOB].[EventFrame].[EventFrame]   | StartTime              | EventFrameSnapshot  | eventframe_start_time        | DateTime | n          | acts as the FILTER WINDOW                                                                            |
| [HOB].[EventFrame].[EventFrame]   | EndTime                | EventFrameSnapshot  | eventframe_end_time          | DateTime | y          | acts as the FILTER WINDOW                                                                            |
| [HOB].[EventFrame].[EventFrame]   | CanBeAcknowledged      | EventFrameSnapshot  | eventframe_can_be_acknowledged | Boolean  | n          |                                                                                                      |
| [HOB].[EventFrame].[EventFrame]   | Acknowledged           | EventFrameSnapshot  | eventframe_acknowledged_on   | DateTime | y          | Rename to AcknowledgedOn for clarity                                                                 |
| [HOB].[EventFrame].[EventFrame]   | AcknowledgedBy         | EventFrameSnapshot  | eventframe_acknowledged_by   | String   | y          |                                                                                                      |
| [HOB].[EventFrame].[EventFrameAttribute] | Name           | EventFrameSnapshot  | eventframe_attribute_name    | String   | n          |                                                                                                      |


Please summarize your understanding so far before we move on with the first task.

## Key Topics Covered

### Data Extraction Options

Considering two approaches to extract data from Aveva PI:
1. Via SQL Server extract using Azure Data Factory (ADF).
2. Using the PI Web API (to avoid architectural and networking dependencies).

### Data and Schema Requirements

- The user has documented the required data and schema in a table format.
- The main fact table of interest is EventFrameSnapshot.
- Several columns come from related tables (EventFrame and EventFrameAttribute), enriching the core facts.

### Schema Differences

- The SQL-based approach has a defined schema, while the PI Web API returns JSON objects, leading to differences that must be reconciled or transformed.

### Primary Columns/Fields Needed

- eventframe_attribute_id
- time
- value
- value_guid
- eventframe_id
- eventframe_name
- eventframe_start_time
- eventframe_end_time
- eventframe_can_be_acknowledged
- eventframe_acknowledged_on
- eventframe_acknowledged_by
- eventframe_attribute_name

Additional context for each column (data type, remarks, etc.) is provided.

### Filtering & Enrichment

- EventFrame’s start_time and end_time act as the filter window.
- Additional columns are included for programmatic enrichment (e.g., for foreign keys and enumerations).

## Conclusion

- You’ve established an approach to leverage the PI Web API to extract the needed data for the EventFrameSnapshot and related tables.
- There is an existing data structure in SQL, but it doesn’t directly map to the JSON-based API from PI. A transformation will be needed.

## Next Steps

1. Align the API outputs with the desired DWH schema.
2. Plan or design the extraction logic using the PI Web API.
3. Validate any transformations needed to match the SQL-based schema requirements.