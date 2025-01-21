# Prod Deployment Meeting Notes 27/11/2024

## Leading Questions
- Does the weekly production push make sense?
- What constitutes as a hotfix?
- Any other guidelines we want to add?

===

- Q: Do we only do hotfixes for the priority reports?
  - A: Operational or *security* issue (whether or not its priority) or if the report breaks

- Recommendation: besides production push, they will also be the support lead for that week
  - 1 support lead
  - 1 person helping who knows the context

## SOP
  - Upon notification of failure
  - Identify criticality: if priority report, if operational/security issue breakage
    - Notify team in chat if critical
  - Communicate to the business that we noticed the failure (by the support lead) (whether or not its critical)
    - TO-DO: Create list of contact people for reports
  - get into contact with person with the context on the situation
  - troubleshoot
  - plan to resolve: internally within a day
  - Communicate upon fix (by the support lead)
  - Post Fix Document Release

Pay attention next week if prod push stops PM report

## Deployment Procedure
1. Full Deploy in TST
2. Environment Transfer
3. Full Deploy in PRD

- Note: Full Deploys are proof of OK builds

To-do:
- Decision Document for SOP whenever report breakage (JL)
- Create template for post fix artifact (JL)
