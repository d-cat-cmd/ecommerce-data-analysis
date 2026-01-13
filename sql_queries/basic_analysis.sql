-- get basic cusotmer info
SELECT * FROM customers LIMIT 10;

-- count customers by city
SELECT city, COUNT(*) AS customer_count 
FROM customers
GROUP BY city
ORDER BY customer_count DESC;

-- get all products with their profit margin
SELECT product_name, category, price, cost,
ROUND(price - cost, 2) AS profit,
ROUND((price - cost) / price * 100, 2) AS profit_percentage
FROM products
ORDER BY profit_percentage DESC;

-- get recent orders with customer names
SELECT 
    o.order_id, 
    o.order_date, 
    c.first_name || ' ' || c.last_name AS customer_name,
    o.status
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC
LIMIT 10;

-- calculate total revenue
SELECT 
    ROUND(SUM(oi.unit_price * oi.quantity), 2) AS total_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = "completed";


-- MORE PRACTICE BELOW, NOT INCLUDED IN run_queries.py
-------------------------------------------------------


-- SELECTING DATA
------------------
-- return customer first names, last names, and cities for first 15 customers
SELECT 
    first_name,
    last_name,
    city
FROM customers
LIMIT 15;

-- return all products with their name, category, price. sort by price high to low
SELECT 
    product_name,
    category,
    price
FROM products
ORDER BY price DESC;

-- show order IDs, order dates, status for 20 most recent orders
SELECT
    order_id,
    order_date,
    status
FROM orders
ORDER BY order_date DESC
LIMIT 20;


-- FILTERING
-------------
-- find all customers who live in New York, show full names and email addresses
SELECT
    first_name || ' ' || last_name AS customer_name,
    email,
    city
FROM customers
WHERE city = 'New York';

-- find products priced between $50 and $200
-- show product name, category, price
-- sort by price from low to high
SELECT  
    product_name,
    category, 
    price
FROM products
WHERE price BETWEEN 50 AND 200
ORDER BY price ASC;

-- find all orders with status 'processing'
-- show order ID, order date, and customer ID
SELECT 
    order_id,
    order_date,
    customer_id,
    status
FROM orders
WHERE status = 'processing';


-- AGGREGATION
---------------
-- count how many customers are in each city
-- show city and the count of customers, sort by customer count descending
SELECT
    COUNT(customer_id),
    city
FROM customers
GROUP BY city
ORDER BY COUNT(customer_id) DESC;

-- count how many products are in each category
-- show category and product count
SELECT
    category,
    COUNT(product_id)
FROM products
GROUP BY category;

-- count how many orders currently have each status
-- show status and order count
SELECT
    status,
    COUNT(order_id)
FROM orders
GROUP BY status;


-- JOINS
---------
-- show orders with customer names, display order_id, order_date, and customer's full name
-- only show completed orders and limit to 10 results
SELECT
    o.status,
    o.order_id,
    o.order_date,
    c.first_name || ' ' || c.last_name AS customer_name
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id
WHERE status = 'completed'
LIMIT 10;

-- show order items with product names
-- display order_id, product_name, quantity, and unit_price
-- limit to 15 results
SELECT  
    oi.order_id,
    p.product_name,
    oi.quantity,
    oi.unit_price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LIMIT 15;


-- DATE FILTERING
------------------
-- find customers who signed up in the last 6 months of 2023
-- show their names and signup dates
-- sort by signup date descending
SELECT
    first_name || ' ' || last_name AS customer_name,
    signup_date
FROM customers
WHERE signup_date BETWEEN '2023-07-01' AND '2023-12-31'
ORDER BY signup_date DESC;

-- find orders placed in the last 30 days of your data
-- show order_id, order_date, and status
SELECT 
    order_id,
    order_date,
    status
FROM orders
WHERE order_date >= (SELECT DATE(MAX(order_date), '-30 days')FROM orders)
ORDER BY order_date DESC;


-- BASIC CALCULATIONS
----------------------
-- calculate the total value of each order
-- for order_items, show order_id and the total (quantity * unit_price) for each item
-- Limit to 10 results
SELECT 
    order_id,
    ROUND(SUM(quantity * unit_price), 2) AS total_order_value
FROM order_items
GROUP BY order_id
LIMIT 10;

-- calculate profit margin for each product
-- show product_name, price, cost, and profit margin percentage 
-- sort from highest profit margin first
SELECT
    product_name,
    price,
    cost,
    ROUND((price-cost)/price*100, 2) AS profit_margin_percentage
FROM products
ORDER BY profit_margin_percentage DESC;