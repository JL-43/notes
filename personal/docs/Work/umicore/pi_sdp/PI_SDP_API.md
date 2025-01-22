# PI SDP API

## Exploration with EventFrameSnapshot

### Initial Message to ChatGPT o1
---
> i am extracting data from aveva pi.
>
> currently, we are exploring the option of extracting the data through a sql server extract with ADF--but architecturally, there are quite a lot of challenges.
>
> to reduce dependency on the work of the architect and network team, i want to leverage the pi web api which is already an available option for me to use.
>
> for the moment, i have defined the data and schema that we need in a document.
>
> the most important "facts" are from a table called "eventframesnapshot."
>
> the schema from sql is not the same as the schema from the apis (perhaps it is to do with the nature of it being json objects? unsure).
>
> but, either way, this is a list of all the columns we need:

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


*Please summarize your understanding so far before we move on with the first task.*
---

### Key Topics Covered

#### Data Extraction Options

Considering two approaches to extract data from Aveva PI:
1. Via SQL Server extract using Azure Data Factory (ADF).
2. Using the PI Web API (to avoid architectural and networking dependencies).

#### Data and Schema Requirements

- The user has documented the required data and schema in a table format.
- The main fact table of interest is EventFrameSnapshot.
- Several columns come from related tables (EventFrame and EventFrameAttribute), enriching the core facts. And making data pull on a time-based condition possible (see: EventFrame.Startime and EventFrame.EndTime)

#### Schema Differences

- The SQL-based approach has a defined schema, while the PI Web API returns JSON objects, leading to differences that must be reconciled or transformed.

#### Primary Columns/Fields Needed

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

#### Filtering & Enrichment

- EventFrame’s start_time and end_time act as the filter window.
- Additional columns are included for programmatic enrichment (e.g., for foreign keys and enumerations).

### Development

#### Repository

We have created a private repository for the scripts:

[Github: PI SDP API](https://github.com/JL-43/pi_sdp_api)

#### Creating Tests

Following the Test-Driven Development methodology, we first created tests to define the expected output of our data extraction scripts.

We were able to define the schema and expected output by leveraging our existing [Functional Document](https://umicore365.sharepoint.com/:x:/r/teams/TWS-002472/_layouts/15/Doc.aspx?sourcedoc=%7B4A3C1A46-63AF-4962-BC8E-AB85AB44CF73%7D&file=PI%20SDP.xlsx&action=default&mobileredirect=true) that describes the different tables we expect, and their schema definitions (See `Tables Schema Sheet`). Besides that, we also provided some mock data by querying in `PI SQL Commander Lite`

####

#### Scratch

We might query the API on time window (starttime and endtime), and eventframeattribute id

Data compare

```
https://azu-as-0066/piwebapi/assetdatabases/F1RDi3nQR9tXEUeItBpeh9IplwhbIFZ1WayEO7dAvzCxOezwSE9CLVBJQUZcSE9C/eventframes

we are looking for:
"eventframesnapshot_attribute_id": "010c96be-0000-0000-8026-000000000000",
"eventframesnapshot_time": "2024-12-16T09:04:00",
"eventframesnapshot_value": "",
"eventframesnapshot_value_guid": "fd54b5be-1d35-4b0d-afd1-10378cbed1ed",
"eventframe_id": "6005f0b9-cfc6-427b-0000-0000010c96be", -- MAYBE 001
"eventframe_name": "DT3 tijdens batch", -- OK 002
"eventframe_starttime": "2024-12-16T09:04:00", -- OK 003
"eventframe_endtime": None, -- OK 004
"eventframe_canbeacknowledged": False,
"eventframe_acknowledgedon": None,
"eventframe_acknowledgedby": None,
"eventframeattribute_id": "010c96a7-0000-0000-e40e-000000000000",
"eventframeattribute_name": "reden Sac"

sample return object:

..., {
      "WebId": "F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0",
      "Id": "79cd2c64-d8b2-11ef-9d60-000d3aafde33", -- event frame id? 001
      "Name": "Analyse Ongeraffineerd Blister", -- event frame name 002
      "Description": "",
      "Path": "\\\\HOB-PIAF\\HOB\\EventFrames[Analyse Ongeraffineerd Blister]",
      "TemplateName": "H26 Analyse",
      "HasChildren": false,
      "CategoryNames": [],
      "ExtendedProperties": {},
      "StartTime": "2025-01-22T11:13:00Z", -- 003
      "EndTime": "2025-01-22T11:43:00Z", -- 004
      "Severity": "None",
      "AcknowledgedBy": "",
      "AcknowledgedDate": "1970-01-01T00:00:00Z",
      "CanBeAcknowledged": false,
      "IsAcknowledged": false,
      "IsAnnotated": false,
      "IsLocked": false,
      "AreValuesCaptured": false,
      "RefElementWebIds": [
        "F1Emi3nQR9tXEUeItBpeh9IplwxPG_u0RN7BGOWdz7SCftewSE9CLVBJQUZcSE9CXFNNRUxURVJcMS4gU01FTFRPVkVOXFNNRUxUT1ZFTg"
      ],
      "Security": {
        "CanAnnotate": true,
        "CanDelete": true,
        "CanExecute": false,
        "CanRead": true,
        "CanReadData": true,
        "CanSubscribe": false,
        "CanSubscribeOthers": false,
        "CanWrite": true,
        "CanWriteData": true,
        "HasAdmin": false,
        "Rights": [
          "ReadWrite",
          "Delete",
          "ReadWriteData",
          "Annotate"
        ]
      },
      "Links": {
        "Self": "https://azu-as-0066/piwebapi/eventframes/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0",
        "Attributes": "https://azu-as-0066/piwebapi/eventframes/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/attributes",
        "EventFrames": "https://azu-as-0066/piwebapi/eventframes/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/eventframes",
        "Database": "https://azu-as-0066/piwebapi/assetdatabases/F1RDi3nQR9tXEUeItBpeh9IplwhbIFZ1WayEO7dAvzCxOezwSE9CLVBJQUZcSE9C",
        "ReferencedElements": "https://azu-as-0066/piwebapi/eventframes/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/referencedelements",
        "PrimaryReferencedElement": "https://azu-as-0066/piwebapi/elements/F1Emi3nQR9tXEUeItBpeh9IplwxPG_u0RN7BGOWdz7SCftewSE9CLVBJQUZcSE9CXFNNRUxURVJcMS4gU01FTFRPVkVOXFNNRUxUT1ZFTg",
        "Template": "https://azu-as-0066/piwebapi/elementtemplates/F1ETi3nQR9tXEUeItBpeh9IplwuAR5j5T_PEOkicGCBN-JYwSE9CLVBJQUZcSE9CXEVMRU1FTlRURU1QTEFURVNbSDI2IEFOQUxZU0Vd",
        "Categories": "https://azu-as-0066/piwebapi/eventframes/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/categories",
        "InterpolatedData": "https://azu-as-0066/piwebapi/streamsets/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/interpolated",
        "RecordedData": "https://azu-as-0066/piwebapi/streamsets/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/recorded",
        "PlotData": "https://azu-as-0066/piwebapi/streamsets/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/plot",
        "SummaryData": "https://azu-as-0066/piwebapi/streamsets/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/summary",
        "Value": "https://azu-as-0066/piwebapi/streamsets/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/value",
        "EndValue": "https://azu-as-0066/piwebapi/streamsets/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/end",
        "Security": "https://azu-as-0066/piwebapi/eventframes/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/security",
        "SecurityEntries": "https://azu-as-0066/piwebapi/eventframes/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/securityentries"
      }
    }, ...
```