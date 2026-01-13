import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# This is an idempotent script to create a database and populate it with fictional ecommerce data
# It will recreate the file "ecommerce.db" from scratch each time it is run

# End result:
# 100 customers with unique emails and realistic data
# 10 products with sale prices and business costs
# Around 300 orders spread across the customers
# Approx. 800 order items linking orders to products

def create_database():
    try:
        # Ensure the databases directory exists
        os.makedirs('../databases', exist_ok=True)
        
        # Connect to SQLite database
        conn = sqlite3.connect('../databases/ecommerce.db')
        
        # Fix for Python 3.12 date deprecation warning, converts dates to ISO format (yyyy-mm-dd)
        def adapt_date(date_val):
            return date_val.isoformat()
        
        sqlite3.register_adapter(datetime, adapt_date)
        sqlite3.register_adapter(datetime.date, adapt_date)
        
        # Create a cursor to execute SQL commands
        cursor = conn.cursor()
        
        print("Connected to database successfully!")
        
        # Read and execute the SQL file to create tables
        try:
            # Safely open and read the SQL file
            with open('../sql_queries/create_tables.sql', 'r') as file: 
                sql_script = file.read()
            # Execute all SQL commands
            cursor.executescript(sql_script)
            print("Tables created successfully!")
        except FileNotFoundError:
            print("SQL file not found. Creating tables manually...")
            # Create tables manually if SQL file doesn't exist
            create_tables_manually(cursor)
        
        # Generate and insert sample data
        print("Generating sample data...")
        
        # Sample data for customers 
        # Calls generate_customer_data() which returns a lsit of customer tuples
        # executemany(): Efficiently inserts all 100 customers at once
        # ? placeholders: Safe way to insert data (prevents SQL injection attacks)
        customers = generate_customer_data()
        cursor.executemany('INSERT INTO customers VALUES (?,?,?,?,?,?,?)', customers)
        print(f"Inserted {len(customers)} customers")
        
        # Sample data for products
        # Hard-coded list of 10 products
        # each tuple contains:(id, name, category, price, cost)
        products = [
            (1, 'Laptop', 'Electronics', 999.99, 650.00),
            (2, 'Smartphone', 'Electronics', 699.99, 450.00),
            (3, 'Headphones', 'Electronics', 149.99, 80.00),
            (4, 'Desk Chair', 'Furniture', 199.99, 120.00),
            (5, 'Coffee Maker', 'Home Appliances', 79.99, 45.00),
            (6, 'Water Bottle', 'Sports', 24.99, 12.00),
            (7, 'Backpack', 'Fashion', 59.99, 35.00),
            (8, 'Book: Data Science', 'Books', 49.99, 25.00),
            (9, 'Monitor', 'Electronics', 299.99, 180.00),
            (10, 'Keyboard', 'Electronics', 89.99, 50.00)
        ]
        cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?)', products)
        print(f"Inserted {len(products)} products")
        
        # Generate orders and order items
        # Calls generate_order_data() to return two lists: orders and order items
        orders, order_items = generate_order_data(customers, products)
        cursor.executemany('INSERT INTO orders VALUES (?,?,?,?)', orders)
        cursor.executemany('INSERT INTO order_items VALUES (?,?,?,?,?)', order_items)
        print(f"Inserted {len(orders)} orders and {len(order_items)} order items")
        
        # Commit and close
        conn.commit()   # Saves all changes to the database
        conn.close()    # Closes the database connection
        print("Database created and populated successfully!")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        # Make sure to close connection even if error occurs
        if 'conn' in locals():
            conn.close()

def create_tables_manually(cursor):
    """Create tables manually if SQL file is missing"""
    tables_sql = [
        """CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE,
            signup_date DATE,
            city TEXT,
            country TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price DECIMAL(10,2),
            cost DECIMAL(10,2)
        )""",
        """CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )""",
        """CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price DECIMAL(10,2),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )"""
    ]
    
    for sql in tables_sql:
        cursor.execute(sql)

# Helper functions

# generate_customer_data:
    # Creates 100 unique customers
    # Email uniqueness: Uses a set() to track used emails and adds numbers if duplicates occur
    # Random dates: Customers sign up randomly throughout 2023
    # Random cities: Picks from the cities list
def generate_customer_data():
    """Generate sample customer data with unique emails"""
    customers = []
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Emily', 'Chris', 'Amanda', 'Brian', 'Nicole']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Moore', 'Taylor', 'Anderson']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    
    # Track used emails to avoid duplicates
    used_emails = set()
    
    for i in range(1, 101):  # 100 customers
        first = random.choice(first_names)
        last = random.choice(last_names)
        
        # Generate unique email
        base_email = f"{first.lower()}.{last.lower()}"
        email = f"{base_email}@email.com"
        counter = 1
        
        # If email already exists, add a number
        while email in used_emails:
            email = f"{base_email}{counter}@email.com"
            counter += 1
        
        used_emails.add(email)
        
        # Convert date to string to avoid deprecation warning
        signup_date = (datetime(2023, 1, 1).date() + timedelta(days=random.randint(0, 365))).isoformat()
        
        customers.append((
            i,  # customer_id
            first,
            last,
            email,
            signup_date,
            random.choice(cities),
            'USA'
        ))
    return customers

# generate_order_data(customers, products):
    # Nested loops:
        # Outer: Goes through each customer
        # Middle: Creates 1-5 orders per customer
        # Inner: Adds 1-4 items to each order
    # Order dates: All orders are from 2024
    # Random products: Each order contains random products with random quantities
def generate_order_data(customers, products):
    """Generate sample order and order item data"""
    orders = []
    order_items = []
    order_id = 1
    order_item_id = 1
    
    for customer in customers:
        customer_id = customer[0]  # First element is customer_id
        # Each customer has 1-5 orders
        for _ in range(random.randint(1, 5)):
            # Convert date to string
            order_date = (datetime(2024, 1, 1).date() + timedelta(days=random.randint(0, 90))).isoformat()
            orders.append((
                order_id,
                customer_id,
                order_date,
                random.choice(['completed', 'completed', 'completed', 'shipped', 'processing'])
            ))
            
            # Each order has 1-4 items
            for _ in range(random.randint(1, 4)):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                order_items.append((
                    order_item_id,
                    order_id,
                    product[0],  # product_id
                    quantity,
                    product[3]   # price
                ))
                order_item_id += 1
            
            order_id += 1
    
    return orders, order_items

if __name__ == "__main__":
    create_database()

# old code below
'''   
def create_database():
    # Connect to SQLite database or create it if it doesn't already exist
    conn = sqlite3.connect('../databases/ecommerce.db')
    cursor = conn.cursor()

    # Read and execute the SQL file to create tables
    with open('../sql_queries/create_tables.sql', 'r') as file:
        sql_script = file.read()
    cursor.executescript(sql_script)

    # Sample data for customers
    customers = []
    first_names = ['Michael', 'Joyce', 'James', 'Lucas', 'Dustin', 'Maxine', 'Steven', 'Edward']
    last_names = ['Wheeler', 'Buyers', 'Hopper', 'Sinclair', 'Henderson', 'Mayfield', 'Harrington', 'Munson']
    cities = ['Los Angeles', 'Indianapolis', 'Anchorage', 'Salt Lake City']

    # creates an empty list "customers" to store data, loops 100 times to create 100 customers
    # for each customer:
        # random.choice(): Picks a random name from our lists
        # f"{first.lower()}.{last.lower()}@email.com": Creates email addresses like "john.smith@email.com"
        # datetime(2023, 1, 1).date() + timedelta(days=random.randint(0, 365)): Creates random signup dates throughout 2023
        # append(): Adds the customer tuple to our list
    for i in range(1, 101): 
        first = random.choice(first_names)
        last = random.choice(last_names)
        customers.append((
            i,
            first,
            last,
            f"{first.lower()}.{last.lower()}@email.com",
            datetime(2023,1,1).date() + timedelta(days=random.randint(0, 365)),
            random.choice(cities),
            'USA'
        ))

    # Sample data for products, manually defines 10 products as tuples
    # Each tuple contains: (product_id, product_name, category, price, cost)
    # Static since products don't change often
    products = [
        (1, 'Laptop', 'Electronics', 999.99, 650.00),
        (2, 'Smartphone', 'Electronics', 699.99, 450.00),
        (3, 'Headphones', 'Electronics', 149.99, 80.00),
        (4, 'Desk Chair', 'Furniture', 199.99, 120.00),
        (5, 'Coffee Maker', 'Home Appliances', 79.99, 45.00),
        (6, 'Water Bottle', 'Sports', 24.99, 12.00),
        (7, 'Backpack', 'Fashion', 59.99, 35.00),
        (8, 'Book: Data Science', 'Books', 49.99, 25.00),
        (9, 'Monitor', 'Electronics', 299.99, 180.00),
        (10, 'Keyboard', 'Electronics', 89.99, 50.00)
    ]

    # Sample orders and order items
    orders = []
    order_items = []
    order_id = 1
    order_item_id = 1

    # Outer loop runs through each customer (1 - 100)
    for customer_id in range (1, 101):
        # Middle loop creates 1 - 5 orders per customer, generates random order dates in 2024
        for _ in range(random.randint(1, 5)):
            order_date = datetime(2024, 1, 1).date() + timedelta(days=random.randint(0, 90))
            orders.append((
                order_id,
                customer_id,
                order_date,
                random.choice(['completed', 'completed', 'completed', 'shipped', 'processing']) # Most orders have already been completed
            ))

            # Inner loop adds 1 - 4 items to each order
            for _ in range(random.randint(1, 4)):
                product = random.choice(products)   # Picks random products
                quantity = random.randint(1, 3)
                order_items.append((
                    order_item_id,
                    order_id,
                    product[0],     # product_id 
                    quantity,
                    product[3]      # price
                ))
                order_item_id += 1
            order_item_id += 1

    # Insert data into tables
    cursor.executemany('INSERT INTO customers VALUES (?,?,?,?,?,?,?)', customers)   # executemany(): Efficiently inserts multiple rows at once
    cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?)', products)         # ? placeholders: Safe way to insert data (prevents SQL injection)
    cursor.executemany('INSERT INTO orders VALUES (?,?,?,?)', orders)               # Each ? gets replaced with values from our tuples
    cursor.executemany('INSERT INTO order_items VALUES (?,?,?,?,?)', order_items)

    # Commit and close
    conn.commit()   # conn.commit(): Saves all changes to the database
    conn.close()    # conn.close(): Closes the database connection
    print("Database created and populated successfully!")

if __name__=="__main__":    # Only runs if the script is executed directly (not imported)
    create_database()
'''