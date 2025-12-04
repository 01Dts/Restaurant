import mysql.connector
from mysql.connector import Error


def create_database_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='dts',
            password='dts'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create the restaurant database"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS restaurant_db")
        print("Database 'restaurant_db' created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()


def create_tables(connection):
    """Create all necessary tables"""
    cursor = connection.cursor()

    # Use the database
    cursor.execute("USE restaurant_db")

    # Create Menu table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            menu_id INT PRIMARY KEY,
            menu_name VARCHAR(50) NOT NULL
        )
    """)

    # Create Category table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            cat_id INT PRIMARY KEY,
            category_name VARCHAR(50) NOT NULL,
            menu_id INT,
            FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
        )
    """)

    # Create Menu Items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            item_id INT PRIMARY KEY,
            item_name VARCHAR(100) NOT NULL,
            cat_id INT,
            menu_id INT,
            size VARCHAR(50),
            price VARCHAR(50),
            FOREIGN KEY (cat_id) REFERENCES category(cat_id),
            FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
        )
    """)

    # Create Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_date DATE NOT NULL,
            order_id INT NOT NULL,
            item_id INT,
            size VARCHAR(20),
            price DECIMAL(10, 5),
            qty INT,
            order_status VARCHAR(20),
            total DECIMAL(10, 5),
            FOREIGN KEY (item_id) REFERENCES menu_items(item_id),
            INDEX idx_order_id (order_id)
        )
    """)

    # Create Payments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            payment_date DATE NOT NULL,
            payment_id INT UNIQUE NOT NULL,
            order_id INT NOT NULL,
            amount_due DECIMAL(10, 5),
            tips DECIMAL(10, 2),
            discount DECIMAL(10, 2),
            total_paid DECIMAL(10, 5),
            payment_type VARCHAR(20),
            payment_status VARCHAR(20),
            INDEX idx_order_id (order_id)
        )
    """)

    connection.commit()
    print("All tables created successfully")
    cursor.close()


def insert_menu_data(connection):
    """Insert menu data"""
    cursor = connection.cursor()
    cursor.execute("USE restaurant_db")

    menu_data = [
        (1, 'Food'),
        (2, 'Drinks')
    ]

    cursor.executemany("""
        INSERT INTO menu (menu_id, menu_name) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE menu_name = VALUES(menu_name)
    """, menu_data)

    connection.commit()
    print("Menu data inserted successfully")
    cursor.close()


def insert_category_data(connection):
    """Insert category data"""
    cursor = connection.cursor()
    cursor.execute("USE restaurant_db")

    category_data = [
        (1, 'Starters', 1),
        (2, 'Soft Drinks', 2),
        (3, 'Mains', 1),
        (4, 'Desserts', 2),
        (5, 'Hot Drinks', 2)
    ]

    cursor.executemany("""
        INSERT INTO category (cat_id, category_name, menu_id) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE category_name = VALUES(category_name)
    """, category_data)

    connection.commit()
    print("Category data inserted successfully")
    cursor.close()


def insert_menu_items_data(connection):
    """Insert menu items data"""
    cursor = connection.cursor()
    cursor.execute("USE restaurant_db")

    menu_items_data = [
        (1, 'Item1', 1, 1, 'Small, Large', '1.50, 2.50'),
        (2, 'Item2', 1, 1, None, '3'),
        (3, 'Item3', 2, 2, None, '2.5'),
        (4, 'Item4', 2, 2, None, '1.5'),
        (5, 'Item5', 2, 1, None, '1'),
        (6, 'Item6', 3, 1, 'Small, Large', '2.50, 3.6'),
        (7, 'Item7', 3, 1, None, '2.5'),
        (8, 'Item8', 4, 2, 'Small, Large', '3.75, 6.5'),
        (9, 'Item9', 4, 2, None, '1.5'),
        (10, 'Item10', 5, 2, None, '2')
    ]

    cursor.executemany("""
        INSERT INTO menu_items (item_id, item_name, cat_id, menu_id, size, price) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE item_name = VALUES(item_name)
    """, menu_items_data)

    connection.commit()
    print("Menu items data inserted successfully")
    cursor.close()


def insert_orders_data(connection):
    """Insert orders data"""
    cursor = connection.cursor()
    cursor.execute("USE restaurant_db")

    orders_data = [
        ('2025-10-01', 10, 2, None, 2.5, 1, 'Completed', 2.5),
        ('2025-10-01', 10, 3, None, 1.5, 2, 'Completed', 3),
        ('2025-10-01', 10, 1, 'Small', 3.75, 1, 'Completed', 3.75),
        ('2025-10-01', 11, 5, None, 2.75, 1, 'Completed', 2.75),
        ('2025-10-01', 11, 6, None, 1.75, 2, 'Completed', 3.5),
        ('2025-10-01', 11, 2, None, 2.5, 1, 'Completed', 2.5),
        ('2025-10-01', 11, 3, None, 3.5, 1, 'Completed', 3.5),
        ('2025-10-01', 11, 4, None, 3.75, 2, 'Completed', 7.5),
        ('2025-10-01', 11, 5, None, 1.5, 1, 'Completed', 1.5),
        ('2025-10-01', 12, 6, 'Large', 5.5, 2, 'Completed', 11),
        ('2025-10-01', 12, 7, None, 2.5, 1, 'Completed', 2.5),
        ('2025-10-01', 12, 1, 'Large', 3.5, 1, 'Completed', 3.5),
        ('2025-10-01', 13, 1, 'Small', 2.75, 2, 'Completed', 5.5),
        ('2025-10-01', 13, 6, 'Small', 1.5, 1, 'Completed', 1.5),
        ('2025-10-01', 13, 8, 'Small', 3.5, 1, 'Completed', 3.5),
        ('2025-10-01', 13, 1, 'Small', 2.5, 2, 'Completed', 5),
        ('2025-10-01', 14, 6, 'Large', 2.75, 1, 'Completed', 2.75),
        ('2025-10-01', 14, 1, 'Large', 2.75655, 2, 'Completed', 5.5131),
        ('2025-10-01', 14, 8, 'Large', 2.75, 2, 'Completed', 5.5),
        ('2025-10-01', 14, 1, 'Large', 2.7556, 2, 'Completed', 5.5112),
        ('2025-10-01', 14, 4, None, 5.5, 1, 'Completed', 5.5),
        ('2025-10-01', 14, 3, None, 2.75, 2, 'Completed', 5.5),
        ('2025-10-01', 14, 2, None, 3.5, 1, 'Completed', 3.5),
        ('2025-10-01', 14, 6, 'Large', 3.015, 3, 'Completed', 9.045),
        ('2025-10-02', 15, 2, None, 2.568, 2, 'Completed', 5.136),
        ('2025-10-03', 16, 6, 'Large', 6.586, 3, 'Completed', 19.758),
        ('2025-10-01', 17, 10, None, 2.5, 1, 'Completed', 2.5),
        ('2025-10-01', 17, 9, None, 2.75636, 1, 'Completed', 2.75636),
        ('2025-10-01', 17, 7, None, 5.63982, 1, 'Completed', 5.63982),
        ('2025-10-05', 18, 1, 'Small', 2.5698, 2, 'Completed', 5.1396),
        ('2025-10-05', 18, 6, 'Small', 5.36245, 2, 'Completed', 10.7249),
        ('2025-10-05', 18, 8, 'Small', 5.23569, 2, 'Completed', 10.47138),
        ('2025-10-01', 19, 2, None, 2.75698, 1, 'Completed', 2.75698),
        ('2025-10-01', 19, 4, None, 2.356, 1, 'Completed', 2.356),
        ('2025-10-01', 19, 5, None, 2.457, 2, 'Completed', 4.914),
        ('2025-10-01', 19, 7, None, 2.6359, 1, 'Completed', 2.6359),
        ('2025-10-01', 19, 9, None, 6.523, 1, 'Completed', 6.523),
        ('2025-10-01', 19, 10, None, 8.5412, 3, 'Completed', 25.6236),
        ('2025-10-01', 19, 6, 'Large', 5.683, 2, 'Completed', 11.366),
        ('2025-10-01', 19, 2, None, 6.3564, 1, 'Completed', 6.3564),
        ('2025-10-01', 19, 5, None, 7.235, 1, 'Completed', 7.235),
        ('2025-10-01', 19, 7, None, 2.365, 1, 'Completed', 2.365),
        ('2025-10-01', 20, 1, 'Large', 2.3658, 1, 'Completed', 2.3658),
        ('2025-10-01', 20, 3, None, 2.356, 1, 'Completed', 2.356),
        ('2025-10-01', 20, 6, 'Large', 1.256, 1, 'Completed', 1.256),
        ('2025-10-01', 20, 4, None, 2.635, 1, 'Completed', 2.635),
        ('2025-10-01', 20, 5, None, 5.21, 1, 'Completed', 5.21),
        ('2025-10-01', 20, 7, None, 6.325, 2, 'Completed', 12.65),
        ('2025-10-01', 20, 8, 'Small', 7.2514, 1, 'Completed', 7.2514),
        ('2025-10-01', 20, 9, None, 2.3999, 1, 'Completed', 2.3999),
        ('2025-10-01', 20, 4, None, 2.356, 3, 'Completed', 7.068),
        ('2025-10-01', 20, 6, 'Small', 4.5326, 2, 'Completed', 9.0652)
    ]

    cursor.executemany("""
        INSERT INTO orders (order_date, order_id, item_id, size, price, qty, order_status, total) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, orders_data)

    connection.commit()
    print(f"Orders data inserted successfully: {cursor.rowcount} rows")
    cursor.close()


def insert_payments_data(connection):
    """Insert payments data"""
    cursor = connection.cursor()
    cursor.execute("USE restaurant_db")

    payments_data = [
        ('2025-10-01', 100, 10, 9.25, 0, 0, 9.25, 'Card', 'Completed'),
        ('2025-10-01', 101, 11, 21.25, 0, 0, 10, 'Cash', 'Completed'),
        ('2025-10-01', 102, 11, 21.25, 0, 0, 11.25, 'Card', 'Completed'),
        ('2025-10-02', 103, 12, 17, 3, 4, 16, 'Card', 'Completed'),
        ('2025-10-03', 104, 13, 15.5, 0, 2, 13.5, 'Card', 'Completed'),
        ('2025-10-01', 105, 14, 42.8193, 0, 0, 20, 'Cash', 'Completed'),
        ('2025-10-01', 106, 14, 42.8193, 0, 0, 22.82, 'Card', 'Completed'),
        ('2025-10-02', 107, 15, 5.136, 0, 0, 5.14, 'Card', 'Refunded'),
        ('2025-10-03', 108, 16, 19.758, 0, 0, 10, 'Cash', 'Completed'),
        ('2025-10-03', 109, 16, 19.758, 0, 0, 9.76, 'Card', 'Completed'),
        ('2025-10-01', 110, 17, 10.8918, 0, 0, 10.9, 'Card', 'Completed'),
        ('2025-10-05', 111, 18, 26.33588, 2, 0, 25, 'Cash', 'Completed'),
        ('2025-10-05', 115, 18, 26.33588, 0, 0, 3.34, 'Card', 'Completed'),
        ('2025-10-01', 116, 19, 72.13188, 0, 0, 50, 'Cash', 'Completed'),
        ('2025-10-01', 119, 19, 72.13188, 0, 0, 22.13, 'Card', 'Completed'),
        ('2025-10-01', 120, 20, 52.2573, 0, 0, 25, 'Cash', 'Completed'),
        ('2025-10-01', 121, 20, 52.2573, 0, 0, 27.28, 'Card', 'Completed')
    ]

    cursor.executemany("""
        INSERT INTO payments (payment_date, payment_id, order_id, amount_due, tips, discount, total_paid, payment_type, payment_status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, payments_data)

    connection.commit()
    print(f"Payments data inserted successfully: {cursor.rowcount} rows")
    cursor.close()


def main():
    """Main function to setup database"""
    print("Starting database setup...")

    # Create connection
    connection = create_database_connection()
    if not connection:
        return

    # Create database
    create_database(connection)

    # Create tables
    create_tables(connection)

    # Insert data
    insert_menu_data(connection)
    insert_category_data(connection)
    insert_menu_items_data(connection)
    insert_orders_data(connection)
    insert_payments_data(connection)

    print("\nDatabase setup completed successfully!")
    connection.close()


if __name__ == "__main__":
    main()