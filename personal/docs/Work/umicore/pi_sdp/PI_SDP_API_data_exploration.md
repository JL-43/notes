# Questions/Observations

It seems like the only values we really have trouble with are the ones related to `eventframeattribute`.

[Event Frames API request link sample](https://azu-as-0066/piwebapi/assetdatabases/F1RDi3nQR9tXEUeItBpeh9IplwhbIFZ1WayEO7dAvzCxOezwSE9CLVBJQUZcSE9C/eventframes)

We are looking for:

- `"eventframesnapshot_attribute_id": "010c96be-0000-0000-8026-000000000000"` -- ?
- `"eventframesnapshot_time": "2024-12-16T09:04:00"` -- ? we still don't know what `time` means even from PI SQL
- `"eventframesnapshot_value": ""` -- OK 008 -- but how to interpret? there are many "values" within -- example: [`Value API request link sample`](https://azu-as-0066/piwebapi/streamsets/F1Fmi3nQR9tXEUeItBpeh9Iplwtmi_TNvN7xGdWQANOkcXKASE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTWzI0VSBHRU1JRERFTERFIFZBTiBHRUxFSURCQUFSSEVJRCBET09SIFA0MTBBL0IgPCA0OTBd/value)
- `"eventframesnapshot_value_guid": "fd54b5be-1d35-4b0d-afd1-10378cbed1ed"` - ?
- `"eventframe_id": "6005f0b9-cfc6-427b-0000-0000010c96be"` -- MAYBE 001
- `"eventframe_name": "DT3 tijdens batch"` -- OK 002
- `"eventframe_starttime": "2024-12-16T09:04:00"` -- OK 003
- `"eventframe_endtime": None` -- OK 004
- `"eventframe_canbeacknowledged": False` -- OK 005
- `"eventframe_acknowledged_on": None` -- OK 006
- `"eventframe_acknowledged_by": None` -- OK 007
- `"eventframeattribute_id": "010c96be-0000-0000-8026-000000000000"` -- same as "eventframesnapshot_attribute_id"
- `"eventframeattribute_name": "reden Sac"` -- ?

## Sample Return Object

```json
{
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
  "AcknowledgedBy": "", -- 007
  "AcknowledgedDate": "1970-01-01T00:00:00Z", -- 006
  "CanBeAcknowledged": false, -- 005
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
    "Value": "https://azu-as-0066/piwebapi/streamsets/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/value", -- 008
    "EndValue": "https://azu-as-0066/piwebapi/streamsets/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/end",
    "Security": "https://azu-as-0066/piwebapi/eventframes/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/security",
    "SecurityEntries": "https://azu-as-0066/piwebapi/eventframes/F1Fmi3nQR9tXEUeItBpeh9IplwZCzNebLY7xGdYAANOq_eMwSE9CLVBJQUZcSE9CXEVWRU5URlJBTUVTW0FOQUxZU0UgT05HRVJBRkZJTkVFUkQgQkxJU1RFUl0/securityentries"
  }
}
```
