-- Create Customers Table
CREATE TABLE IF NOT EXISTS customers (  -- Creates a new table only if it doesn't already exist (prevents errors)
    customer_id INTEGER PRIMARY KEY,    -- Unique identifier for each customer, INTEGER = whole number, PRIMARY KEY = uniquely identifies each record and auto-increments
    first_name TEXT NOT NULL,           -- NOT NULL = this field must have a value (can't be empty)
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,                  -- UNIQUE = no two customers can have the same email
    signup_date DATE,                   -- signup_date DATE: Stores dates in YYYY-MM-DD format
    city TEXT,
    country TEXT
);

-- Create Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price DECIMAL (10,2),               -- DECIMAL(10,2) = decimal number with 10 total digits, 2 after decimal. Example: 999.99 (max value: 9999999.99)
    cost DECIMAL (10, 2)
    );

-- Create Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) 
);
-- FOREIGN KEY (customer_id) REFERENCES customers(customer_id): 
    -- Creates a relationship between orders and customers
    -- Ensures customer_id in orders table exists in customers table
    -- Prevents orphan records (orders without customers)

-- Create Order Items table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);