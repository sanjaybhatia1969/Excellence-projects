"""
Database Connection Manager for Café Retail Management System
Handles MySQL connection and basic operations
"""

import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Tuple, Any

class DatabaseConnection:
    """Singleton pattern for database connection"""
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._connection is None:
            self.connect()
    
    def connect(self, with_database=True):
        """Establish connection to MySQL database"""
        try:
            if with_database:
                self._connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='12345',  # Change this to your MySQL password
                    database='cafe_retail_db',
                    autocommit=False
                )
            else:
                # Connect without selecting a database (for initial setup)
                self._connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='12345',  # Change this to your MySQL password
                    autocommit=False
                )
            
            if self._connection.is_connected():
                print("Successfully connected to MySQL server")
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            print("\nPlease check:")
            print("1. MySQL server is running")
            print("2. Username and password are correct in database.py")
            self._connection = None
            return False
    
    def get_connection(self):
        """Get the database connection"""
        if self._connection is None or not self._connection.is_connected():
            self.connect()
        return self._connection
    
    def execute_query(self, query: str, params: Tuple = None) -> bool:
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            if self._connection is None or not self._connection.is_connected():
                self.connect()
            
            if self._connection is None:
                print("Failed to establish database connection")
                return False
            
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self._connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            if self._connection:
                self._connection.rollback()
            return False
    
    def fetch_one(self, query: str, params: Tuple = None) -> Optional[Tuple]:
        """Fetch single record"""
        try:
            if self._connection is None or not self._connection.is_connected():
                self.connect()
            
            if self._connection is None:
                print("Failed to establish database connection")
                return None
            
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
    
    def fetch_all(self, query: str, params: Tuple = None) -> List[Tuple]:
        """Fetch all records"""
        try:
            if self._connection is None or not self._connection.is_connected():
                self.connect()
            
            if self._connection is None:
                print("Failed to establish database connection")
                return []
            
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
    
    def get_last_insert_id(self) -> int:
        """Get last inserted ID"""
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Error as e:
            print(f"Error getting last insert ID: {e}")
            return 0
    
    def close(self):
        """Close database connection"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Database connection closed")


def initialize_database():
    """Create database and tables if they don't exist"""
    conn = None
    cursor = None
    
    try:
        print("Connecting to MySQL server...")
        # Connect without database first to create it
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345'  # Change this to your MySQL password
        )
        
        if not conn.is_connected():
            print("Failed to connect to MySQL server")
            return False
        
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        print("Creating database 'cafe_retail_db' if it doesn't exist...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS cafe_retail_db")
        print("✓ Database created/verified")
        
        # Use the database
        cursor.execute("USE cafe_retail_db")
        print("✓ Using database 'cafe_retail_db'")
        
        # Create Users table
        print("Creating 'users' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'staff') NOT NULL,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Users table created")
        
        # Create Customers table
        print("Creating 'customers' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                address TEXT,
                customer_type ENUM('Regular', 'VIP', 'Student') DEFAULT 'Regular',
                loyalty_points INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Customers table created")
        
        # Create Products table
        print("Creating 'products' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                stock_quantity INT NOT NULL DEFAULT 0,
                low_stock_threshold INT DEFAULT 10,
                category VARCHAR(50),
                is_service BOOLEAN DEFAULT FALSE,
                service_duration INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Products table created")
        
        # Create Transactions table
        print("Creating 'transactions' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                user_id INT NOT NULL,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                subtotal DECIMAL(10, 2) NOT NULL,
                discount_amount DECIMAL(10, 2) DEFAULT 0,
                tax_amount DECIMAL(10, 2) NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                payment_method ENUM('Cash', 'Credit', 'Debit', 'Other') NOT NULL,
                cash_received DECIMAL(10, 2),
                change_given DECIMAL(10, 2),
                status ENUM('Completed', 'Refunded', 'Partial Refund') DEFAULT 'Completed',
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        print("✓ Transactions table created")
        
        # Create Transaction Items table
        print("Creating 'transaction_items' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transaction_items (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                transaction_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10, 2) NOT NULL,
                subtotal DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        print("✓ Transaction Items table created")
        
        # Insert default admin user if not exists
        print("Checking default users...")
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO users (username, password, role, name, email, phone)
                VALUES ('admin', 'admin123', 'admin', 'Administrator', 'admin@cafe.com', '1234567890')
            """)
            print("✓ Default admin user created (username: admin, password: admin123)")
        else:
            print("✓ Admin user already exists")
        
        # Insert default staff user
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'staff'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO users (username, password, role, name, email, phone)
                VALUES ('staff', 'staff123', 'staff', 'Staff Member', 'staff@cafe.com', '0987654321')
            """)
            print("✓ Default staff user created (username: staff, password: staff123)")
        else:
            print("✓ Staff user already exists")
        
        # Insert sample products
        print("Checking sample products...")
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            sample_products = [
                ('Espresso', 'Strong black coffee', 3.50, 100, 10, 'Coffee', 0, 0),
                ('Cappuccino', 'Espresso with steamed milk', 4.50, 100, 10, 'Coffee', 0, 0),
                ('Latte', 'Espresso with more milk', 4.75, 100, 10, 'Coffee', 0, 0),
                ('Americano', 'Espresso with hot water', 3.75, 100, 10, 'Coffee', 0, 0),
                ('Mocha', 'Espresso with chocolate', 5.00, 80, 10, 'Coffee', 0, 0),
                ('Croissant', 'Buttery pastry', 3.00, 50, 5, 'Pastry', 0, 0),
                ('Muffin', 'Blueberry muffin', 3.25, 40, 5, 'Pastry', 0, 0),
                ('Bagel', 'Fresh bagel', 2.50, 60, 5, 'Pastry', 0, 0),
                ('Sandwich', 'Ham and cheese sandwich', 6.50, 30, 5, 'Food', 0, 0),
                ('Salad', 'Fresh garden salad', 7.00, 25, 5, 'Food', 0, 0),
                ('Green Tea', 'Hot green tea', 2.50, 80, 10, 'Tea', 0, 0),
                ('Black Tea', 'Hot black tea', 2.50, 80, 10, 'Tea', 0, 0),
                ('Iced Coffee', 'Cold brew coffee', 4.00, 60, 10, 'Coffee', 0, 0),
                ('Smoothie', 'Fruit smoothie', 5.50, 40, 5, 'Beverage', 0, 0),
                ('Orange Juice', 'Fresh orange juice', 3.50, 50, 10, 'Beverage', 0, 0),
            ]
            cursor.executemany("""
                INSERT INTO products (name, description, price, stock_quantity, 
                                    low_stock_threshold, category, is_service, service_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, sample_products)
            print(f"✓ {len(sample_products)} sample products added")
        else:
            print("✓ Products already exist in database")
        
        conn.commit()
        print("\n" + "="*50)
        print("✓ Database initialization completed successfully!")
        print("="*50)
        
        return True
        
    except Error as e:
        print(f"\n❌ Error initializing database: {e}")
        if conn:
            conn.rollback()
        return False
    
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("Database connection closed")


if __name__ == "__main__":
    initialize_database()
