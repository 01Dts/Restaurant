import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    try:
        return mysql.connector.connect(**Config.DB_CONFIG)
    except Error as e:
        print(f"MySQL Connection Error: {e}")
        return None
