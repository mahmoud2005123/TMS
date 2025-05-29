import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mahmoud',
            database='training_mm'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return None

def verify_connection():
    try:
        print("Attempting to connect to the database...")
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"Successfully connected to database: {db_name}")
            
            # التحقق من وجود الجداول
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("Available tables:", [table[0] for table in tables])
            
            # التحقق من هيكل جدول الطلاب
            cursor.execute("DESCRIBE students")
            columns = cursor.fetchall()
            print("Students table structure:")
            for column in columns:
                print(f"- {column[0]}: {column[1]}")
            
            connection.close()
            return True
    except Error as e:
        print(f"Error verifying database: {e}")
        return False

def init_database():
    try:
        print("Attempting to connect to MySQL server...")
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mahmoud'
        )
        
        if connection.is_connected():
            print("Connected to MySQL server successfully!")
            cursor = connection.cursor()
            
            # Create and use database
            print("Creating database...")
            cursor.execute("DROP DATABASE IF EXISTS training_mm")
            cursor.execute("CREATE DATABASE training_mm")
            cursor.execute("USE training_mm")
            print("Database 'training_mm' selected!")
            
            # Create students table
            print("Creating students table...")
            cursor.execute("""
                CREATE TABLE students ( 
                    student_id INT PRIMARY KEY, 
                    student_name VARCHAR(100) NOT NULL, 
                    program VARCHAR(100) NOT NULL, 
                    enrollment_year INT CHECK (enrollment_year BETWEEN 2015 AND 2025), 
                    cgpa DECIMAL(3,2) CHECK (cgpa >= 0.00 AND cgpa <= 4.00),
                    email VARCHAR(100) UNIQUE,
                    phone VARCHAR(15)
                )
            """)
            
            # Create organizations table
            print("Creating organizations table...")
            cursor.execute("""
                CREATE TABLE organizations ( 
                    organization_id INT PRIMARY KEY, 
                    organization_name VARCHAR(100) NOT NULL UNIQUE, 
                    location VARCHAR(100) NOT NULL 
                )
            """)
            
            # Create internal_supervisors table
            print("Creating internal supervisors table...")
            cursor.execute("""
                CREATE TABLE internal_supervisors ( 
                    supervisor_id INT PRIMARY KEY, 
                    supervisor_name VARCHAR(100) NOT NULL, 
                    department VARCHAR(100) NOT NULL 
                )
            """)
            
            # Create external_supervisors table
            print("Creating external supervisors table...")
            cursor.execute("""
                CREATE TABLE external_supervisors ( 
                    supervisor_id INT PRIMARY KEY, 
                    supervisor_name VARCHAR(100) NOT NULL, 
                    organization_id INT NOT NULL, 
                    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id) 
                )
            """)
            
            # Create training_reports table
            print("Creating training reports table...")
            cursor.execute("""
                CREATE TABLE training_reports ( 
                    report_id INT PRIMARY KEY, 
                    student_id INT NOT NULL, 
                    organization_id INT NOT NULL, 
                    report_date DATE NOT NULL CHECK (report_date BETWEEN '2023-01-01' AND '2023-12-31'), 
                    report_text VARCHAR(1000) NOT NULL, 
                    FOREIGN KEY (student_id) REFERENCES students(student_id), 
                    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id) 
                )
            """)
            
            # Create evaluations table
            print("Creating evaluations table...")
            cursor.execute("""
                CREATE TABLE evaluations ( 
                    evaluation_id INT PRIMARY KEY, 
                    report_id INT NOT NULL, 
                    supervisor_id INT NOT NULL, 
                    evaluation_date DATE NOT NULL CHECK (evaluation_date BETWEEN '2023-01-01' AND '2023-12-31'), 
                    evaluation_score DECIMAL(5,2) CHECK (evaluation_score BETWEEN 0.00 AND 100.00), 
                    evaluation_comments VARCHAR(1000), 
                    FOREIGN KEY (report_id) REFERENCES training_reports(report_id), 
                    FOREIGN KEY (supervisor_id) REFERENCES internal_supervisors(supervisor_id) 
                )
            """)
            
            # Create users table with role field for compatibility
            print("Creating users table...")
            cursor.execute("""
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    role ENUM('admin', 'trainer', 'trainee', 'supervisor') NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert sample data
            print("Inserting sample data...")
            
            # Insert students
            cursor.execute("""
                INSERT INTO students (student_id, student_name, program, enrollment_year, cgpa, email, phone) VALUES
                (1001, 'Ahmed Ali', 'Computer Science', 2020, 3.5, 'ahmed.ali@example.com', '01234567890'),
                (1002, 'Sara Khaled', 'Business', 2019, 3.8, 'sara.k@example.com', '01234567891'),
                (1003, 'Mohamed Tarek', 'Engineering', 2021, 2.9, 'mohamed.t@example.com', '01234567892'),
                (1004, 'Laila Hassan', 'Pharmacy', 2020, 3.2, 'laila.h@example.com', '01234567893'),
                (1005, 'Omar Adel', 'Law', 2022, 3.7, 'omar.a@example.com', '01234567894'),
                (1006, 'Mona Youssef', 'Architecture', 2019, 3.1, 'mona.y@example.com', '01234567895'),
                (1007, 'Khaled Nabil', 'Economics', 2021, 2.8, 'khaled.n@example.com', '01234567896'),
                (1008, 'Nour Hany', 'Medicine', 2020, 3.9, 'nour.h@example.com', '01234567897'),
                (1009, 'Youssef Gamal', 'IT', 2022, 3.3, 'youssef.g@example.com', '01234567898'),
                (1010, 'Salma Ehab', 'Dentistry', 2019, 3.0, 'salma.e@example.com', '01234567899')
            """)
            
            # Insert organizations
            cursor.execute("""
                INSERT INTO organizations (organization_id, organization_name, location) VALUES
                (1, 'Tech Corp', 'Cairo'),
                (2, 'MediHealth', 'Alexandria'),
                (3, 'BuildSmart', 'Giza')
            """)
            
            # Insert internal supervisors
            cursor.execute("""
                INSERT INTO internal_supervisors (supervisor_id, supervisor_name, department) VALUES
                (1, 'Dr. Ahmed Sameer', 'Computer Science'),
                (2, 'Dr. Maha Nasr', 'Business')
            """)
            
            # Insert external supervisors
            cursor.execute("""
                INSERT INTO external_supervisors (supervisor_id, supervisor_name, organization_id) VALUES
                (1, 'Eng. Hani Maher', 1),
                (2, 'Dr. Rania Shawky', 2)
            """)
            
            # Insert training reports
            cursor.execute("""
                INSERT INTO training_reports (report_id, student_id, organization_id, report_date, report_text) VALUES
                (1, 1001, 1, '2023-06-15', 'Worked on backend systems.'),
                (2, 1002, 2, '2023-07-10', 'Handled market analysis.')
            """)
            
            # Insert evaluations
            cursor.execute("""
                INSERT INTO evaluations (evaluation_id, report_id, supervisor_id, evaluation_date, evaluation_score, evaluation_comments) VALUES
                (1, 1, 1, '2023-06-20', 85.5, 'Good technical skills'),
                (2, 2, 2, '2023-07-15', 90.0, 'Excellent performance')
            """)
            
            # Insert admin user
            cursor.execute("""
                INSERT INTO users (username, password, full_name, email, role) VALUES 
                ('admin', 'admin123', 'System Administrator', 'admin@training.com', 'admin')
            """)
            
            connection.commit()
            print("Database and tables created successfully!")
            
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    init_database()
