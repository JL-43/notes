# Umicore-AVEVA Meeting on EF Data Ingestion
**Date: February 18, 2025**

## Agenda
Post-implementation of PI EF Data Ingestion via Azure Data Factory, the Umicore team consulted AVEVA technical advisors for a "stamp of approval" on their current approach to ingest the data into a data warehouse solution

## Data Volume Analysis
Current event frame data statistics:
- Total EF count: 46,747,338
- Total EF attribute count: 1,164,630
- Total EF count in database: 13,575,235
- Average EF count per day: 16,801
- Median EF count per day: 5,208.5
- Max EF count by day: 6,814,052 (Nov 29, 2022) - flagged as potential outlier by Umicore PI team

*Note: Counts based on last update date, not start/end times*

## Top EF Counts by Day (More Realistic Results)
| Day | Month | Year | EF Count |
|-----|-------|------|---------|
| 29  | 11    | 2022 | 6,814,052 |
| 22  | 9     | 2023 | 2,092,898 |
| 2   | 4     | 2024 | 103,405  |
| 15  | 9     | 2023 | 88,594   |
| 22  | 5     | 2024 | 55,437   |
| 3   | 5     | 2023 | 39,836   |
| 4   | 12    | 2023 | 28,865   |
| 29  | 1     | 2025 | 28,466   |
| 30  | 1     | 2025 | 21,257   |
| 6   | 1     | 2025 | 20,773   |

## Design Considerations
### Database Maintenance
- Re-index database
- Recapture event frame values
- Delete or archive old event frames

### Key Design Questions
- Which event frame attribute values to capture? All or specific ones?
- How to retrieve changes:
  - Periodic batch requests
  - ID-based database diff approach
- Define "frozen horizon" for synchronization
- Synchronization frequency
- Consider automatic and manual backfilling
- PI authentication methods

## Long-term Option: AVEVA CONNECT Data Services
- Expected availability: Q2 2025
- SaaS solution hosted by AVEVA
- **Current limitations (Feb 2025):**
  - Event frame replication not generally available
  - Acknowledgement/annotations not included 
  - Events not available in data views/virtual tables
- Concerns raised about public data source implications

## Access Method Comparison

### .NET AFSDK
**Pros:**
- Direct data access
- FindChanges() method available
- Can recapture event frame values

**Cons:**
- Requires development work
- Uses .NET Framework 4

**Authentication:**
- Kerberos
- OpenID Connect (PI 2023+)

### PI ODBC Driver
**Pros:**
- Supported by Azure Data Factory integration runtime

**Cons:**
- Cannot detect changes
- Requires middleman service
- Legacy component

**Authentication:**
- Kerberos (not supported by ADF)
- Basic

### PI OLEDB Enterprise
**Pros:**
- PI SQL DAS not required

**Cons:**
- Cannot detect changes
- Requires middleman service
- Legacy component

**Authentication:**
- Kerberos
- Basic

### PI Web API
**Pros:**
- Supported by Azure Data Factory integration runtime
- Can recapture event frame values

**Cons:**
- Cannot detect changes
- Requires middleman service

**Authentication:**
- Kerberos (not supported by ADF)
- Basic
- OpenID Connect (PI 2023+)

## Performance Comparison
- .NET approach: 11,500 events in 2 seconds
- SQL approach: 11,500 events in 12 seconds
- ODBC approach: 11,500 events in 13 seconds
- REST approach: 11,500 events in 17 seconds

## Test Architecture
**Environment:**
- PI OLEDB Enterprise Server: 20 GB, 16 CPUs
- PI AF Server
- PI Web API: 6 GB, 4 CPUs
- Test dataset: 22M event frames, ~12K event frames/day, 5 attributes per event frame

## AVEVA Recommendations
1. For handling changes to event frames:
   - ID delta approach is viable
   - Consider using PI SDK table that shows deltas of event frames

2. Regarding annotations and acknowledgements:
   - Modern methods lack support for EF acknowledgement and annotations
   - Recommendation to move from annotations to manual entry into event frame attributes

3. Connection methods:
   - ODBC: More direct, less governance (last updated 2017-2018)
   - OLEDB: More recently updated but requires SQL Server middleman
     - Ensure linked server specs are adequate (generally robust)

4. Implementation guidance:
   - Configure appropriate timeouts and retries
   - Consider "frozen horizons" for synchronization boundaries

## Umicore Decision

Considering the following factors:

- PMR team maturity is building in SQL
- PMR SQL Server is robust
- Annotations are necessary input (totally eliminates other solutions except OLEDB and ODBC)
  - Annotations are considered by Aveva as an overlooked input field
  - They recommend to move the input into EventFrameAttributes instead to use the other solutions
- According to Infrastructure 2.0, the supported Data Ingestion methods are either through an API or Azure Data Factory

With these in mind, Aveva supports the approach implemented by the team

`ODBC -> Linked Server -> Self Hosted Integration Runtime (on the same machine as the Linked Server) -> Expose to Azure Data Factory -> Ingest`