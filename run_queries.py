import sqlite3
import pandas as pd

def run_basic_queries():
    # Connect to database
    conn = sqlite3.connect('../databases/ecommerce.db')
    
    print("=== E-COMMERCE DATA ANALYSIS ===\n")

    # query 1: count customers by city
    query1 = '''
    SELECT 
        city, 
        COUNT(*) AS customer_count 
    FROM customers
    GROUP BY city
    ORDER BY customer_count DESC;
    '''
    df1 = pd.read_sql_query(query1, conn)
    print("1. Number of Customers per City: ")
    print(df1.to_string(index=False))
    print("\n" + "="*50 + "\n")

    # query 2: get all products with their profit margin
    query2 = '''
    SELECT 
        product_name, 
        category, 
        price, 
        cost,
        ROUND(price - cost, 2) AS profit,
        ROUND((price - cost) / price * 100, 2) AS profit_percentage
    FROM products
    ORDER BY profit_percentage DESC;
    '''
    df2 = pd.read_sql_query(query2, conn)
    print("2. Profit Margins for Products: ")
    print(df2.to_string(index=False))
    print("\n" + "="*50 + "\n")

    # query 3: list 10 most recent orders with customer names
    query3 = '''
    SELECT 
        o.order_id, 
        o.order_date, 
        c.first_name || ' ' || c.last_name AS customer_name,
        o.status
    FROM orders o 
    JOIN customers c ON o.customer_id = c.customer_id
    ORDER BY o.order_date DESC
    LIMIT 10;
    '''
    df3 = pd.read_sql_query(query3, conn)
    print("3. 10 Most Recent Orders with Customer Names: ")
    print(df3.to_string(index=False))
    print("\n" + "="*50 + "\n")

    # query 4: calculate total revenue
    query4 = '''
    SELECT 
        ROUND(SUM(oi.unit_price * oi.quantity), 2) AS total_revenue
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = "completed";
    '''
    df4 = pd.read_sql_query(query4, conn)
    print("4. Total Revenue: ")
    print(df4.to_string(index=False))
    print("\n" + "="*50 + "\n")

    conn.close()

if __name__=="__main__":
    run_basic_queries()