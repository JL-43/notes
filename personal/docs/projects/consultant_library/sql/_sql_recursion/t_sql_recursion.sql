-- incomplete

-- sql server / tsql
with cte_1 (iteration) as (
  -- base case
  select 1 as iteration

  union all

  -- recursive case
  select iteration+1
  from cte_1
  where iteration < 3 -- stopping condition
)
select iteration
from cte_1
order by iteration

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

-- add use cases:
-- according to comments, seems like this is very relevant for hierarchical data structures

-- "i have used it a lot for hierarchical data, such as when you want to know how many employees are under managers all the way down (1 to n levels away from the manager)."