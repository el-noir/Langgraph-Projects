import sqlite3
import os
from pathlib import Path

def create_sample_database():
    """Create a sample SQLite database with realistic business data"""
    
    # Create the database file path
    db_path = Path(__file__).parent.parent.parent / "data" / "sample_business.db"
    
    # Create data directory if it doesn't exist
    db_path.parent.mkdir(exist_ok=True)
    
    # Remove existing database if it exists
    if db_path.exists():
        os.remove(db_path)
    
    # Connect to SQLite database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create tables
    # Employees table
    cursor.execute('''
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            salary DECIMAL(10,2) NOT NULL,
            hire_date DATE NOT NULL,
            manager_id INTEGER,
            FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
        )
    ''')
    
    # Products table
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            cost DECIMAL(10,2) NOT NULL,
            stock_quantity INTEGER NOT NULL,
            supplier TEXT NOT NULL,
            created_date DATE NOT NULL
        )
    ''')
    
    # Customers table
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            country TEXT NOT NULL,
            registration_date DATE NOT NULL
        )
    ''')
    
    # Sales table
    cursor.execute('''
        CREATE TABLE sales (
            sale_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            sale_date DATE NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    
    # Insert sample data
    # Employees
    employees_data = [
        (1, 'John', 'Smith', 'john.smith@company.com', 'Sales', 'Sales Manager', 75000.00, '2022-01-15', None),
        (2, 'Sarah', 'Johnson', 'sarah.johnson@company.com', 'Sales', 'Sales Representative', 45000.00, '2022-03-20', 1),
        (3, 'Mike', 'Davis', 'mike.davis@company.com', 'Sales', 'Sales Representative', 47000.00, '2022-02-10', 1),
        (4, 'Emily', 'Brown', 'emily.brown@company.com', 'Engineering', 'Software Engineer', 85000.00, '2021-11-05', None),
        (5, 'David', 'Wilson', 'david.wilson@company.com', 'Engineering', 'Senior Developer', 95000.00, '2021-08-12', None),
        (6, 'Lisa', 'Anderson', 'lisa.anderson@company.com', 'Marketing', 'Marketing Manager', 70000.00, '2022-04-01', None),
        (7, 'Tom', 'Taylor', 'tom.taylor@company.com', 'Marketing', 'Marketing Specialist', 50000.00, '2022-06-15', 6),
        (8, 'Jessica', 'Miller', 'jessica.miller@company.com', 'HR', 'HR Manager', 68000.00, '2021-12-20', None)
    ]
    
    cursor.executemany('''
        INSERT INTO employees (employee_id, first_name, last_name, email, department, 
                             position, salary, hire_date, manager_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', employees_data)
    
    # Products
    products_data = [
        (1, 'Laptop Pro 15"', 'Electronics', 1299.99, 800.00, 50, 'TechSupplier Inc', '2023-01-10'),
        (2, 'Wireless Mouse', 'Electronics', 29.99, 15.00, 200, 'AccessoryWorld', '2023-01-15'),
        (3, 'Office Chair', 'Furniture', 299.99, 180.00, 75, 'FurniturePlus', '2023-02-01'),
        (4, 'Standing Desk', 'Furniture', 599.99, 350.00, 30, 'FurniturePlus', '2023-02-15'),
        (5, 'Coffee Maker', 'Appliances', 89.99, 45.00, 100, 'KitchenPro', '2023-03-01'),
        (6, 'Bluetooth Headphones', 'Electronics', 199.99, 120.00, 80, 'AudioTech', '2023-03-10'),
        (7, 'Desk Lamp', 'Office Supplies', 49.99, 25.00, 150, 'OfficeMax', '2023-03-20'),
        (8, 'Water Bottle', 'Accessories', 24.99, 8.00, 300, 'EcoProducts', '2023-04-01')
    ]
    
    cursor.executemany('''
        INSERT INTO products (product_id, product_name, category, price, cost, 
                            stock_quantity, supplier, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', products_data)
    
    # Customers
    customers_data = [
        (1, 'Alice', 'Cooper', 'alice.cooper@email.com', '555-0101', 'New York', 'NY', 'USA', '2023-01-05'),
        (2, 'Bob', 'Williams', 'bob.williams@email.com', '555-0102', 'Los Angeles', 'CA', 'USA', '2023-01-12'),
        (3, 'Carol', 'Jones', 'carol.jones@email.com', '555-0103', 'Chicago', 'IL', 'USA', '2023-02-03'),
        (4, 'Daniel', 'Garcia', 'daniel.garcia@email.com', '555-0104', 'Houston', 'TX', 'USA', '2023-02-15'),
        (5, 'Eva', 'Martinez', 'eva.martinez@email.com', '555-0105', 'Phoenix', 'AZ', 'USA', '2023-03-01'),
        (6, 'Frank', 'Rodriguez', 'frank.rodriguez@email.com', '555-0106', 'Philadelphia', 'PA', 'USA', '2023-03-10'),
        (7, 'Grace', 'Lewis', 'grace.lewis@email.com', '555-0107', 'San Antonio', 'TX', 'USA', '2023-04-05'),
        (8, 'Henry', 'Lee', 'henry.lee@email.com', '555-0108', 'San Diego', 'CA', 'USA', '2023-04-12')
    ]
    
    cursor.executemany('''
        INSERT INTO customers (customer_id, first_name, last_name, email, phone, 
                             city, state, country, registration_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', customers_data)
    
    # Sales
    sales_data = [
        (1, 1, 2, 1, 1, 1299.99, 1299.99, '2023-04-10'),
        (2, 2, 2, 2, 2, 29.99, 59.98, '2023-04-11'),
        (3, 3, 3, 3, 1, 299.99, 299.99, '2023-04-12'),
        (4, 1, 2, 6, 1, 199.99, 199.99, '2023-04-13'),
        (5, 4, 3, 4, 1, 599.99, 599.99, '2023-04-14'),
        (6, 5, 2, 5, 1, 89.99, 89.99, '2023-04-15'),
        (7, 6, 3, 7, 3, 49.99, 149.97, '2023-04-16'),
        (8, 7, 2, 8, 5, 24.99, 124.95, '2023-04-17'),
        (9, 8, 3, 1, 1, 1299.99, 1299.99, '2023-04-18'),
        (10, 2, 2, 2, 1, 29.99, 29.99, '2023-04-19'),
        (11, 3, 3, 6, 2, 199.99, 399.98, '2023-04-20'),
        (12, 4, 2, 5, 2, 89.99, 179.98, '2023-04-21'),
        (13, 1, 3, 7, 1, 49.99, 49.99, '2023-04-22'),
        (14, 5, 2, 3, 1, 299.99, 299.99, '2023-04-23'),
        (15, 6, 3, 4, 1, 599.99, 599.99, '2023-04-24')
    ]
    
    cursor.executemany('''
        INSERT INTO sales (sale_id, customer_id, employee_id, product_id, quantity, 
                         unit_price, total_amount, sale_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', sales_data)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Sample database created successfully at: {db_path}")
    return str(db_path)

def get_database_schema():
    """Get the database schema information for the LLM"""
    db_path = Path(__file__).parent.parent.parent / "data" / "sample_business.db"
    
    if not db_path.exists():
        raise FileNotFoundError("Database not found. Please run create_sample_database() first.")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Get table information
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema_info[table_name] = columns
    
    conn.close()
    return schema_info

def get_schema_description():
    """Get a human-readable description of the database schema"""
    schema_info = get_database_schema()
    
    description = "Database Schema:\\n\\n"
    
    for table_name, columns in schema_info.items():
        description += f"Table: {table_name}\\n"
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, primary_key = col
            pk_indicator = " (PRIMARY KEY)" if primary_key else ""
            null_indicator = " NOT NULL" if not_null else ""
            description += f"  - {col_name}: {col_type}{pk_indicator}{null_indicator}\\n"
        description += "\\n"
    
    description += """
Sample Business Database Description:
- employees: Company staff information including salary, department, and manager relationships
- products: Product catalog with pricing, inventory, and supplier information  
- customers: Customer contact and location information
- sales: Transaction records linking customers, employees, and products with sales data

Common queries you can ask:
- "What are the top selling products?"
- "Which employees have the highest sales?"
- "Show me sales by department"
- "What's the average salary by department?"
- "Which customers bought the most expensive items?"
"""
    
    return description

if __name__ == "__main__":
    # Create the database
    db_path = create_sample_database()
    
    # Display schema
    print("\\n" + get_schema_description())
