-- might be ansi sql? unsure

with recursive cte_1 as (
  -- base case
  (select 1 as iteration)

  union all

  -- each recursive case
  (
    select iteration + 1 as iteration
    from cte_1
    where iteration < 3 -- stopping condition
  )
)
select iteration
from cte_1
order by 1;