# E-commerce Data Visualisation Script
# Creates professional charts and graphs from SQL database 

# What we are practicing:
# 1. Database Connections: Always open and close connections properly
# 2. SQL in Python: Use parameterised queries to prevent SQL injection
# 3. Chart Types: Different charts for different purposes:
#   Line charts for trends over time
#   Bar charts for comparisons
#   Pie charts for proportions
# 4. Customisation: Professional charts need thoughtful styling
# 5. Error Handling: Use try/except/finally for robustness
# 6. Code Organisation: Functions make code reusable and readable

import sqlite3  # For connecting to our SQLite database
import pandas as pd  # For data manipulation and analysis
import matplotlib.pyplot as plt  # For creating static visualisations
import seaborn as sns  # For making matplotlib charts look nicer
from datetime import datetime  # For date handling (though we're using SQL dates)
import numpy as np  # For numerical operations (used in colour generation)

def setup_plot_styling():
    """
    Configure professional styling for all charts
    This makes our visualisations look polished and consistent
    """
    plt.style.use('seaborn-v0_8')  # Use a clean, modern style template
    sns.set_palette("husl")  # Set a colour palette that's colourblind-friendly
    
    # Configure global plot settings
    plt.rcParams['figure.figsize'] = (12, 8)  # Default chart size (width, height in inches)
    plt.rcParams['font.size'] = 12  # Base font size
    plt.rcParams['axes.titlesize'] = 16  # Title font size
    plt.rcParams['axes.labelsize'] = 14  # Axis label font size
    # These settings ensure all charts have consistent styling

def get_monthly_revenue(conn):
    """
    Extract monthly revenue data from the database
    This query groups sales by month and calculates total revenue
    """
    query = """
    SELECT 
        strftime('%Y-%m', o.order_date) as month,  -- Extract year-month from date
        ROUND(SUM(oi.quantity * oi.unit_price), 2) as monthly_revenue  -- Calculate total revenue per month
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id  -- Connect orders to their items
    WHERE o.status = 'completed'  -- Only count completed orders
    GROUP BY month  -- Group by month to get monthly totals
    ORDER BY month;  -- Sort chronologically
    """
    # pd.read_sql_query executes the SQL and returns a pandas DataFrame
    return pd.read_sql_query(query, conn)

def get_top_products(conn, limit=10):
    """
    Get the top-selling products by revenue
    This helps identify which products are most popular
    """
    query = """
    SELECT 
        p.product_name,
        p.category,
        SUM(oi.quantity) as total_quantity_sold,  -- Total units sold
        ROUND(SUM(oi.quantity * oi.unit_price), 2) as total_revenue  -- Total revenue generated
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id  -- Link products to order items
    JOIN orders o ON oi.order_id = o.order_id  -- Link to orders to check status
    WHERE o.status = 'completed'  -- Only count completed orders
    GROUP BY p.product_id  -- Group by product to aggregate sales
    ORDER BY total_revenue DESC  -- Sort by highest revenue first
    LIMIT ?;  -- Limit to top N products (parameterised for safety)
    """
    # The params=(limit,) replaces the ? in the query - prevents SQL injection
    return pd.read_sql_query(query, conn, params=(limit,))

def get_customer_geography(conn):
    """
    Get customer distribution across different cities
    Useful for understanding market penetration
    """
    query = """
    SELECT 
        city,
        COUNT(*) as customer_count  -- Count customers in each city
    FROM customers 
    GROUP BY city  -- Group by city to get per-city counts
    ORDER BY customer_count DESC;  -- Sort by most customers first
    """
    return pd.read_sql_query(query, conn)

def get_category_performance(conn):
    """
    Get total revenue by product category
    Helps understand which categories drive the most business
    """
    query = """
    SELECT 
        p.category,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) as total_revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY p.category  -- Group by category instead of individual products
    ORDER BY total_revenue DESC;  -- Highest revenue categories first
    """
    return pd.read_sql_query(query, conn)

def plot_monthly_revenue(conn, save_path='../visualisations/monthly_revenue.png'):
    """
    Create a line chart showing revenue trends over time
    Line charts are ideal for showing trends and patterns over time
    """
    # Get the data from database
    df = get_monthly_revenue(conn)
    
    # Create a new figure with specific size
    plt.figure(figsize=(14, 8))
    
    # Create the line plot with customisation
    plt.plot(df['month'], df['monthly_revenue'],  # X and Y data
             marker='o',         # Add circles at each data point
             linewidth=2.5,      # Make line thicker
             markersize=8,       # Size of the circle markers
             color='#2E86AB',    # Custom blue colour
             label='Monthly Revenue')  # For legend (though we're not showing one)
    
    # Customise chart appearance
    plt.title('Monthly Revenue Trend', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=14, fontweight='bold')
    plt.ylabel('Revenue ($)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)  # Add light grid lines for readability
    plt.xticks(rotation=45)    # Rotate x-axis labels so they don't overlap
    
    # Add value labels on each data point for clarity
    for i, (month, revenue) in enumerate(zip(df['month'], df['monthly_revenue'])):
        plt.annotate(f'${revenue:,.0f}',  # Format number with commas
                    (month, revenue),     # Position to annotate
                    textcoords="offset points",  # Position relative to point
                    xytext=(0,10),       # 10 points above the point
                    ha='center',         # Center the text horizontally
                    fontsize=10)         # Slightly smaller font
    
    # Adjust layout to prevent label cutting off and save
    plt.tight_layout()  # Automatically adjust subplot parameters
    plt.savefig(save_path, dpi=300, bbox_inches='tight')  # High resolution, tight borders
    plt.show()  # Display the chart
    
    print(f"Monthly revenue chart saved to: {save_path}")
    return df  # Return data in case we want to use it later

def plot_top_products(conn, save_path='../visualisations/top_products.png'):
    """
    Create a horizontal bar chart of top-selling products
    Horizontal bars work well when you have long product names
    """
    df = get_top_products(conn)
    
    plt.figure(figsize=(14, 10))
    
    # Create horizontal bar chart (barh instead of bar)
    bars = plt.barh(df['product_name'], df['total_revenue'], 
                    color='#A23B72',  # Custom purple colour
                    alpha=0.8)        # Slight transparency
    
    # Customise the chart
    plt.title('Top Selling Products by Revenue', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Total Revenue ($)', fontsize=14, fontweight='bold')
    plt.ylabel('Product Name', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()  # Put highest revenue at top (reverse natural order)
    
    # Add value labels on the end of each bar
    for bar, revenue in zip(bars, df['total_revenue']):
        width = bar.get_width()  # Get the length of the bar
        plt.text(width + max(df['total_revenue']) * 0.01,  # Position just past bar end
                bar.get_y() + bar.get_height()/2,          # Center vertically on bar
                f'${revenue:,.0f}',                        # Formatted revenue
                ha='left', va='center', fontsize=11)       # Left aligned, centered
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Top products chart saved to: {save_path}")
    return df

def plot_revenue_by_category(conn, save_path='../visualisations/revenue_by_category.png'):
    """
    Create a pie chart showing revenue distribution across categories
    Pie charts work well for showing proportions of a whole
    """
    df = get_category_performance(conn)
    
    plt.figure(figsize=(12, 10))
    
    # Generate distinct colours for each category
    # np.linspace creates evenly spaced numbers that we use for colours
    colours = plt.cm.Set3(np.linspace(0, 1, len(df)))
    
    # Create pie chart with multiple customisations
    wedges, texts, autotexts = plt.pie(df['total_revenue'],  # Data to plot
                                      labels=df['category'],  # Category labels
                                      autopct='%1.1f%%',      # Format percentages
                                      colors=colours,        # Our colour array
                                      startangle=90,          # Start first slice at top
                                      textprops={'fontsize': 12})  # Label font size
    
    plt.title('Revenue Distribution by Product Category', 
              fontsize=18, fontweight='bold', pad=20)
    
    # Improve percentage labels to be more readable
    for autotext in autotexts:
        autotext.set_color('white')      # White text on coloured background
        autotext.set_fontweight('bold')  # Bold for better visibility
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Category revenue chart saved to: {save_path}")
    return df

def plot_customer_geography(conn, save_path='../visualisations/customer_geography.png'):
    """
    Create a bar chart showing customer distribution across cities
    Bar charts are ideal for comparing quantities across categories
    """
    df = get_customer_geography(conn)
    
    plt.figure(figsize=(14, 8))
    
    # Create vertical bar chart
    bars = plt.bar(df['city'], df['customer_count'], 
                   color='#F18F01',  # Custom orange colour
                   alpha=0.8)        # Slight transparency
    
    # Customise the chart
    plt.title('Customer Distribution by City', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('City', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Customers', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)  # Rotate city names for readability
    
    # Add value labels on top of each bar
    for bar, count in zip(bars, df['customer_count']):
        height = bar.get_height()  # Get the height of the bar
        plt.text(bar.get_x() + bar.get_width()/2.,  # Center horizontally on bar
                height + 0.5,                       # Slightly above the bar
                f'{count}',                         # The count value
                ha='center', va='bottom', fontsize=11)  # Centered, at bottom of text
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Customer geography chart saved to: {save_path}")
    return df

def create_all_visualisations():
    """
    Main function that orchestrates the creation of all visualisations
    This is the function you call to generate your entire portfolio of charts
    """
    # Establish database connection - this creates a link to our SQLite file
    conn = sqlite3.connect('../databases/ecommerce.db')
    
    print("🎨 Creating Data Visualisations...\n")
    
    try:
        # Create each visualisation one by one with progress updates
        print("1. 📈 Creating Monthly Revenue Trend...")
        revenue_data = plot_monthly_revenue(conn)
        
        print("\n2. 📊 Creating Top Products Chart...")
        products_data = plot_top_products(conn)
        
        print("\n3. 🥧 Creating Revenue by Category Chart...")
        category_data = plot_revenue_by_category(conn)
        
        print("\n4. 🌎 Creating Customer Geography Chart...")
        geography_data = plot_customer_geography(conn)
        
        print("\n✅ All visualisations completed successfully!")
        print("📁 Charts saved to the 'visualisations' folder")
        
        # Return all the dataframes in case we want to do further analysis
        return {
            'revenue': revenue_data,
            'products': products_data,
            'categories': category_data,
            'geography': geography_data
        }
        
    except Exception as e:
        # If anything goes wrong, this will catch the error and show us what happened
        print(f"❌ Error creating visualisations: {e}")
        return None
        
    finally:
        # This block always runs, even if there's an error
        # Ensures we don't leave database connections open
        conn.close()

if __name__ == "__main__":
    """
    This block only runs when we execute the script directly
    It won't run if we import this file as a module
    """
    # Execute the main function and get back our data
    data_results = create_all_visualisations()
    
    # Optional: Print a quick summary of what we found
    if data_results:
        print("\n" + "="*50)
        print("📊 QUICK SUMMARY")
        print("="*50)
        total_revenue = data_results['revenue']['monthly_revenue'].sum()
        total_customers = data_results['geography']['customer_count'].sum()
        print(f"Total Revenue: ${total_revenue:,.2f}")
        print(f"Total Customers: {total_customers}")
        print(f"Top Product: {data_results['products'].iloc[0]['product_name']}")
        print(f"Top Category: {data_results['categories'].iloc[0]['category']}")