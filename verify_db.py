import mysql.connector
from mysql.connector import Error

def verify_database():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mahmoud',
            database='training_mm'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\nTables in database:")
            for table in tables:
                print(f"- {table[0]}")
                
            # Check admin user
            print("\nChecking admin user:")
            cursor.execute("SELECT username, full_name, role FROM users WHERE username='admin'")
            admin = cursor.fetchone()
            if admin:
                print(f"Admin user exists: {admin}")
            
            # Check table structures
            for table in tables:
                print(f"\nStructure of {table[0]} table:")
                cursor.execute(f"DESCRIBE {table[0]}")
                columns = cursor.fetchall()
                for column in columns:
                    print(f"- {column[0]}: {column[1]}")
                    
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    verify_database() 