# Mindmap

## PI Web API VS SQL Linked Servers
- Ine had mentioned that she would prefer the PI API way of working as she thinks the option to work with the linked server is not production-grade
  - Linked Server route: 
    - `+` No need for an application layer if we just do a database-to-database connection. 
    - `+` Leverage database user security instead of managing API endpoint credentials and tokens
    - `-` API mentioned as the future "way-of-working"
      - This is from a data-access POV though and not really for lifting a large amount of historical data from one db to another
    - `-` PI team was previously able to work with linked servers, but this workflow had been removed
      - Reason for removal might be an unforeseen challenge
  
### ![alt text](image-1.png)[Microsoft Documentation: Linked Servers](https://learn.microsoft.com/en-us/sql/relational-databases/linked-servers/linked-servers-database-engine?view=sql-server-ver16)

### Questions:
  - Any context we are blind to that has umicore enforcing PI Web API as the defacto way of communicating with PI?
  - Currently we are pulling from views created in PI SQL Commander Lite -> If we are to move to APIs for consistency, do we need to re-do?
  - Moving to an API way of working would enforce to be API devs over Data Engineers
    - Working with APIs VS working with Databases
- If we are to proceed with linked service, we need some backing to convince `Jeroen De Wolf` as well

## TimeXtender Stabilization

### Deploying and running priority reports in test to check for stability
- [x] - PI
- [x] - PI - DSA
- [x] - PI - MDW
- [x] - PM No SS
- [x] - PM No SS - DSA
- [x] - PM No SS - MDW
- [ ] - Safety
- [ ] - Safety - DSA
- [ ] - Safety - MDW -> (Safety Requires changes)
- [x] - Lead Refinery
- [x] - Lead Refinery - DSA
- [x] - Lead Refinery - MDW

### Victor has validated the priority execution packages last Friday. 
- After 1 more week of stable runs & no reporting mishaps, recommend to delete old execution packages

### Department Dim Migration
- What is Department SP URL?
- Remap safety

### Plant Maintenance Snapshots

#### Plan A: Reducing Load Times
- [TimeXtender: Troubleshooting data cleansing rules](https://support.timextender.com/prepare-90/troubleshooting-data-cleansing-rules-883)
  - Above article also references: [TimeXtender: Batch cleansing option - best practices, tips and tricks](https://support.timextender.com/prepare-90/batch-cleansing-option-best-practices-tips-and-tricks-792)
  
#### Plan B: Plant Maintenance Snapshots
- Take a look at lead refinery snapshot and see if it can be implemented for plant maintenance