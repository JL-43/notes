We have created the initial availability report with the business called "SAC"

The availability report from SAC is taking its data from PI with the following view that the PI team generated for us

```sql
 --TOP 1(ef.ID),
 ef.ID,
ef.Name,
CASE
WHEN ef.Name NOT LIKE 'Batch' AND ef.Name NOT LIKE 'DT1 %' THEN 'SubEvent'
ELSE 'Event'
END AS EventType,
ef.StartTime,
ef.EndTime,
ef.Acknowledged,
ef.AcknowledgedBy,
'' AS Comment,
--efan.Comment,
--ROW_NUMBER() OVER (PARTITION BY ef.Name ORDER BY ef.ID DESC) rn,
ef.PrimaryReferencedElementID,
MAX(CASE
WHEN efa.Name = 'Lotnummer' THEN CAST(s.Value AS String)
END) AS Lotnummer,
MAX(CASE
WHEN efa.Name = 'Reden Sac' THEN CAST(s.Value AS String)
END) AS [Reden Sac],
MAX(CASE
WHEN efa.Name = 'Tarra Gewicht' THEN CAST(s.Value AS String)
END) AS TarraGewicht
FROM [HOB].[EventFrame].[EventFrame] ef
INNER JOIN [HOB].[EventFrame].[EventFrameAttribute] efa
ON efa.EventFrameID = ef.ID
INNER JOIN [HOB].[Data].[EventFrameSnapshot] s
ON s.EventFrameAttributeID = efa.ID
LEFT JOIN [HOB].[EventFrame].[EventFrameAnnotation] efan
ON efan.EventFrameID = ef.ID
WHERE
ef.PrimaryReferencedElementID IN
(
'e1383ed5-7635-11ed-a827-04cf4bd5aed9'
,'b3bb86f5-886f-11ee-a861-04cf4bd5aed9'
,'65c61183-9368-11ee-a865-04cf4bd5aed9'
,'03d0e7d7-504e-11ed-a4b2-aced5c1957b6'
,'e1383ed5-7635-11ed-a827-04cf4bd5aed9'
,'d6a80719-bb83-11ee-a86a-04cf4bd5aed9'
,'09cd99ce-bb84-11ee-a86a-04cf4bd5aed9'
,'171ce7ec-bb84-11ee-a86a-04cf4bd5aed9'
,'1dbbc2b9-9049-11ef-a891-04cf4bd5aed9'
)
AND efa.Name IN ('Lotnummer','Reden Sac','Tarra Gewicht')
--AND WHERE row_number = 1
--and startTime > '*-10d'
GROUP BY ef.ID,
ef.Name,
ef.PrimaryReferencedElementID,
ef.StartTime,
ef.EndTime,
ef.Acknowledged,
ef.AcknowledgedBy--,
--efan.Comment
```

SAC availability report was built on our 1.0 infrastructure

We want now to "generalize" the SAC availability report as SAC is not the only business that needs the availability report

Availability report in general will be using these tables (please properly convert these into a markdown table as well)

Table Name	Table Location	isFact?	incrementalLoadCapable?	count as of 21/11/2024	remarks
Annotation	*cannot find at the moment*				
EventFrameCategory	[HOB].[EventFrame].[EventFrameCategory]	-	Y		heavy query by itself, has to use the "predefined query" option = does this query have everything they need?
EventFrames	[HOB].[EventFrame].[EventFrame]	Y	Y	3266005	
ElementHierarchy	[HOB].[Asset].[ElementHierarchy]	N	N		how deep into the hierarchy are we going?
EventFrameAttribute	[HOB].[EventFrame].[EventFrameAttribute]	-	-	-	heavy query by itself, has to use the "predefined query" option = does this query have everything they need?
EventFrameTemplate	[HOB].[EventFrame].[EventFrameTemplate]	N	N	1894	
EventFrameSnapshot	[HOB].[Data].[EventFrameSnapshot]	-	-	-	MAIN FACT TABLE. heavy query by itself, has to use the "predefined query" option = does this query have everything they need?
EventFrameTemplateAttribute	[HOB].[EventFrame].[EventFrameTemplateAttribute]	N		4261	
EnumerationSet	[HOB].[Asset].[EnumerationSet]	N	Y	225	
EnumerationValue	[HOB].[Asset].[EnumerationValue]	N	Y	4561	adds detail to enumerationset. join on enumerationsetID

The objective is we want to use the learning we have from building SAC availability report to generalize and properly make an ETL pipeline for all the other availability reports

The business also that the availability report belongs to can also be identified by this section in the where clause

```sql
WHERE
ef.PrimaryReferencedElementID IN
(
'e1383ed5-7635-11ed-a827-04cf4bd5aed9'
,'b3bb86f5-886f-11ee-a861-04cf4bd5aed9'
,'65c61183-9368-11ee-a865-04cf4bd5aed9'
,'03d0e7d7-504e-11ed-a4b2-aced5c1957b6'
,'e1383ed5-7635-11ed-a827-04cf4bd5aed9'
,'d6a80719-bb83-11ee-a86a-04cf4bd5aed9'
,'09cd99ce-bb84-11ee-a86a-04cf4bd5aed9'
,'171ce7ec-bb84-11ee-a86a-04cf4bd5aed9'
,'1dbbc2b9-9049-11ef-a891-04cf4bd5aed9'
)
```

these are all the equipment that belong to SAC

in the future, the PI team will create it in such a way that we just indicate "SAC" and it will return the proper installations. This is not our job

the challenges are that the following tables are very heavy to query

[HOB].[EventFrame].[EventFrameCategory]
[HOB].[EventFrame].[EventFrameAttribute]
[HOB].[Data].[EventFrameSnapshot]

and we dont know if they are all capable of incremental load (for some of them, i was just looking if they had the "modified on" field for us to base incremental load from)