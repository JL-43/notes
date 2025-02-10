Objective

Create F_Safety view in MDW

Why?

- DSA.VW_NOTIFICATIONCENTER getting errors. This is because the department mapping no longer exists (deleted, existed in DSA). The newly implemented department dim is available only in MDW as a team decision
- Logic for joins moved to MDW View instead, to explicilty handlye logic
- Currently, bulk of the logic is in MDW.DW_F_SAFETY (table)
  - Originally, the table is taking from the following tables:
    - DSA.F_SAFETY_NOTIFICATION (FACT)
    - DSA.Eerste zorgen & Ongevallen
    - DSA.OBSERVATIE_CPM_S
    - DSA.VW_NOTIFICATIONCENTER
    - DSA.VW_INCIDENT
    - DSA.INCIDENT

MDW.DW_F_SAFETY original columns
DSA.F_SAFETY_NOTIFICATION.NotificationNo as Safety_Key


Strategy

- Pull apart the tables and logic used in MDW.DW_F_SAFETY
- Apply the logic in MDW.VW_F_SAFETY instead