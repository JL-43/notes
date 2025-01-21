/*
 * Description:
 *  This example demonstrates how to use recursion in SQL using Common Table Expressions (CTEs).
 *  It includes basic recursion and a practical use case for hierarchical data, such as employee-manager relationships.
 *
 * FAQ:
 *  - What is a recursive CTE?
 *    A recursive CTE is a CTE that references itself, allowing you to perform iterative calculations or traverse hierarchical structures.
 *
 *  - What is the base case?
 *    The base case initializes the recursion by providing a starting point for the iteration.
 *
 *  - What is the stopping condition?
 *    The stopping condition ensures the recursion terminates by limiting the depth of recursion, avoiding infinite loops.
 *
 *  - Where is recursion commonly used?
 *    Recursion is particularly useful for hierarchical data structures, such as organizational charts, folder structures, or dependency trees.
 */

-- Basic Recursion Example
-- SQL Server (T-SQL)
with cte_1 (iteration) as (
  -- Base case
  select 1 as iteration

  union all

  -- Recursive case
  select iteration + 1
  from cte_1
  where iteration < 3 -- Stopping condition
)
select iteration
from cte_1
order by iteration;

-- Practical Use Case: Hierarchical Data
-- Example: Employee-Manager Relationship

-- Sample Data Table
create table employees (
    employee_id int,
    employee_name varchar(100),
    manager_id int -- References employee_id
);

-- Insert Sample Data
insert into employees (employee_id, employee_name, manager_id) values
(1, 'CEO', null),
(2, 'VP of Sales', 1),
(3, 'Sales Manager', 2),
(4, 'Sales Associate', 3),
(5, 'VP of Engineering', 1),
(6, 'Engineering Manager', 5),
(7, 'Software Engineer', 6);

-- Recursive Query to Find All Subordinates of a Given Manager
-- Example: Find all employees under the CEO (employee_id = 1)
with employee_hierarchy (employee_id, employee_name, manager_id, level) as (
  -- Base case: Start with the manager
  select
    employee_id,
    employee_name,
    manager_id,
    1 as level
  from employees
  where manager_id is null -- Assuming top-level manager has null manager_id

  union all

  -- Recursive case: Find direct reports of the current level
  select
    e.employee_id,
    e.employee_name,
    e.manager_id,
    eh.level + 1 as level
  from employees e
  inner join employee_hierarchy eh on e.manager_id = eh.employee_id
)
select *
from employee_hierarchy
order by level, employee_id;

/*
 * Notes:
 *  - The "level" column indicates the depth in the hierarchy.
 *  - Adjust the base case filter to target a specific manager or top-level node.
 *
 * Test this logic to understand how recursive CTEs can traverse hierarchies and aggregate results.
 */
