import sqlite3

# Test script to check that database has data and returns the tables and numbers of records

def test_connection():
    # Connect to the database
    conn = sqlite3.connect('../databases/ecommerce.db')
    cursor = conn.cursor()
    
    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # create table, a temporary variable that takes on each value in the tables list one at a time
    # First iteration: table = ('customers',)
    # Second iteration: table = ('products',)
    print("Tables in the database:")
    for table in tables:
        print(f" - {table[0]}") 
        # table[0] accesses the first element of the tuple, in this case the table name
        # iterations do not change table[0] to table[1] etc. but the data in table[0] changes
    
    # Count records in each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f" - {table_name}: {count} records")
    
    conn.close()

if __name__ == "__main__":
    test_connection()