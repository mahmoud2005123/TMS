import mysql.connector
from mysql.connector import Error

def test_mysql_connection():
    try:
        print("Testing MySQL connection...")
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mahmoud'
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    test_mysql_connection() 