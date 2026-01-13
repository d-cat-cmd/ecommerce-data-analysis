-- New SQL Concepts for Intermediate Queries

-- 1. HAVING Clause
-- Purpose: Filter groups after aggregation (WHERE filters rows before aggregation)

-- Basic structure
SELECT column, aggregate_function(column)
FROM table
GROUP BY column
HAVING aggregate_function(column) condition;


-- 2. Subqueries in WHERE Clause
-- Purpose: Use the result of one query as a condition in another

-- Example: Find customers who spent more than average
SELECT customer_id, total_spent
FROM (
    SELECT customer_id, SUM(amount) as total_spent
    FROM orders 
    GROUP BY customer_id
) 
WHERE total_spent > (SELECT AVG(amount) FROM orders);


-- 3. Common Table Expressions (CTEs) - WITH clause
-- Purpose: Create temporary named result sets that you can reference later

-- Basic structure
WITH cte_name AS (
    SELECT columns
    FROM table
    WHERE conditions
)
SELECT * FROM cte_name;


-- 4. Window Functions
-- Purpose: Perform calculations across a set of table rows related to the current row

-- Example: Running total
SELECT 
    order_date,
    revenue,
    SUM(revenue) OVER (ORDER BY order_date) as running_total
FROM monthly_revenue;


-- 5. LAG() and LEAD() Functions
-- Purpose: Access data from previous/next rows in the same result set

-- LAG: Get previous row's value
LAG(column, 1) OVER (ORDER BY ordering_column)
-- LEAD: Get next row's value  
LEAD(column, 1) OVER (ORDER BY ordering_column)


-- 6. CASE Statements
-- Purpose: Conditional logic in SQL (like if/then/else)

-- Basic structure
CASE 
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE default_result
END


-- 7. Date Functions
-- Purpose: Extract parts of dates or calculate date differences

-- SQLite date functions
strftime('%Y-%m', date_column)  -- Extract year-month
date('now')                     -- Current date
julianday(date1) - julianday(date2)  -- Days between dates


-- 8. EXISTS Operator
-- Purpose: Check if a subquery returns any rows

SELECT column
FROM table
WHERE EXISTS (subquery);


-- 9. Self Joins
-- Purpose: Join a table to itself (useful for comparing rows within same table)

SELECT a.column, b.column
FROM table a
JOIN table b ON a.common_column = b.common_column;


-- PRACTICE QUERIES
--------------------

-- Find customers who have placed more than 3 orders
-- Show customer name and order count
-- Use GROUP BY, HAVING, and JOIN
SELECT  
    c.customer_id,
    c.first_name || ' '|| c.last_name AS customer_name,
    COUNT(o.order_id) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id  -- as this is unique and names are not
HAVING COUNT(order_id) > 3
ORDER BY total_orders DESC;

-- Calculate average order value by customer city
-- Show city and average order value
-- Multiple JOINs and GROUP BY 
SELECT 
    c.city,
    ROUND(AVG(oi.quantity * oi.unit_price), 2) AS avg_item_value,
    (SELECT ROUND(AVG(order_totals.total_value), 2)
    FROM (
        SELECT 
            o2.order_id, 
            SUM(oi2.quantity * oi2.unit_price) AS total_value
        FROM orders o2
        JOIN order_items oi2 ON o2.order_id = oi2.order_id
        JOIN customers c2 ON o2.customer_id = c2.customer_id
        WHERE c2.city = c.city
        GROUP BY o2.order_id
    ) order_totals) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.city;

-- Find products that have never been ordered
-- Show product name and category
-- Use a LEFT JOIN and look for NULL values
SELECT 
    p.product_name,
    p.category
FROM products p     -- starting from all products in our catalogue
LEFT JOIN order_items oi ON p.product_id = oi.product_id 
WHERE oi.product_id IS NULL; -- filter for only the products that have no order items

-- Calculate monthly revenue growth percentage
-- Show month, revenue, and growth from previous month
-- Hint: Use a CTE with LAG() window function
WITH monthly_revenue AS ( 
    SELECT 
        strftime('%Y-%m', o.order_date) AS month, -- create a month column
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS monthly_revenue -- calculating montlhy revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY month
    ORDER BY month
)
SELECT
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month) AS previous_month_revenue,
    ROUND (
        (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month))* 100.0 /
        LAG(monthly_revenue) OVER (ORDER BY month), 2) AS growth_percentage
FROM monthly_revenue
ORDER BY month;

-- Find customers with the highest average order value
-- Show customer name and average order value
-- Only include customers with at least 2 orders
-- Hint: use HAVING clause with aggregate function

--Step 1: Calculate Each Customer's Average Order Value
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    AVG(/* order total calculation*/) AS avg_order_value,
    COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY c.customer_id;

-- Step 2: Add the Order Count Filter
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    AVG(/* order total calculation*/) AS avg_order_value,
    COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY c.customer_id
HAVING order_count >= 2;

-- Step 3: Calculate Order Totals Properly
SELECT 
    order_id,
    ROUND(SUM(quantity * unit_price), 2) AS total_order_value
FROM order_items
GROUP BY order_id
LIMIT 10;