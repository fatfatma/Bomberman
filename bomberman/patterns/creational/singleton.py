# patterns/creational/singleton.py
"""
Singleton Pattern - Database Connection
Ensures only one database connection instance exists throughout the application
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class DatabaseConnection:
    """
    Singleton class for managing database connection.
    Only one instance of database connection will exist.
    """
    _instance = None
    _connection = None

    def __new__(cls):
        """
        Override __new__ to control object creation.
        Returns the same instance if it already exists.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def get_connection(self):
        """
        Returns the database connection.
        Creates a new connection if one doesn't exist.
        """
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(**DB_CONFIG)
                print("✅ Database connection established (Singleton)")
            except Error as e:
                print(f"❌ Database connection error: {e}")
                return None
        return self._connection

    def close_connection(self):
        """Close the database connection"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("🔒 Database connection closed")


# Usage Example:
if __name__ == "__main__":
    # Test Singleton Pattern
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()

    print(f"db1 is db2: {db1 is db2}")  # Should print True

    conn = db1.get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        print(f"Connected to database: {result}")
        cursor.close()