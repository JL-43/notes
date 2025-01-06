/*
 * Description:
 *  This example demonstrates how to pivot (and optionally unpivot) data using CTEs.
 *  It transforms a "tall" table of monthly sales into a "wide" format, with separate
 *  columns for each month. You can adapt this snippet for any set of pivot columns
 *  or different grouping levels by modifying the WITH clauses and the pivot logic.
*/

with original_table as ( -- * tall table
  select
    customer_id,
    month_name, -- * e.g. 'jan', 'feb', 'mar', ...
    sales_amount
  from monthly_sales
), 

pivoted_table as (
  select
    customer_id,
    [jan] as jan_sales, 
    [feb] as feb_sales,
    [mar] as mar_sales, 
    [apr] as apr_sales, 
    [may] as may_sales, 
    [jun] as jun_sales, 
    [jul] as jul_sales, 
    [aug] as aug_sales, 
    [sep] as sep_sales, 
    [oct] as oct_sales, 
    [nov] as nov_sales, 
    [dec] as dec_sales
  from
    original_table
  pivot (
    sum(sales_amount)
    for month_name in (
      [jan], 
      [feb],
      [mar], 
      [apr], 
      [may], 
      [jun], 
      [jul], 
      [aug], 
      [sep], 
      [oct], 
      [nov], 
      [dec]
    )
  ) as p
),
-- * Extra: if the goal is to "unpivot" a table:
unpivoted_table as (
    select
        customer_id,
        month_name,
        sales_amount
    from pivoted_table
    unpivot (
        sales_amount for month_name in (
          [jan_sales], 
          [feb_sales], 
          [mar_sales], 
          [apr_sales], 
          [may_sales], 
          [jun_sales], 
          [jul_sales], 
          [aug_sales], 
          [sep_sales], 
          [oct_sales], 
          [nov_sales], 
          [dec_sales])
    ) as u
)

select
    *
from pivoted_table;

-- * Test the logic yourself:

-- * -- create table
create table monthly_sales (
    customer_id int,
    month_name varchar(3),
    sales_amount decimal(10, 2)
);

-- * -- insert dummy data

insert into monthly_sales (customer_id, month_name, sales_amount) VALUES
(1, 'jan', 100.00), (1, 'feb', 150.00), (1, 'mar', 200.00), (1, 'apr', 250.00), (1, 'may', 300.00), (1, 'jun', 350.00), (1, 'jul', 400.00), (1, 'aug', 450.00), (1, 'sep', 500.00), (1, 'oct', 550.00), (1, 'nov', 600.00), (1, 'dec', 650.00),
(2, 'jan', 120.00), (2, 'feb', 180.00), (2, 'mar', 240.00), (2, 'apr', 260.00), (2, 'may', 320.00), (2, 'jun', 380.00), (2, 'jul', 440.00), (2, 'aug', 500.00), (2, 'sep', 560.00), (2, 'oct', 620.00), (2, 'nov', 680.00), (2, 'dec', 740.00),
(3, 'jan', 130.00), (3, 'feb', 170.00), (3, 'mar', 210.00), (3, 'apr', 270.00), (3, 'may', 330.00), (3, 'jun', 390.00), (3, 'jul', 450.00), (3, 'aug', 510.00), (3, 'sep', 570.00), (3, 'oct', 630.00), (3, 'nov', 690.00), (3, 'dec', 750.00);