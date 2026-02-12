# database/repository.py
"""
Repository Pattern - Base Repository
Abstracts database operations and provides a clean interface
"""

from abc import ABC, abstractmethod
from patterns.creational.singleton import DatabaseConnection


class Repository(ABC):
    """
    Abstract base repository class.
    All repositories inherit from this class.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def get_connection(self):
        """Get database connection"""
        return self.db.get_connection()

    def execute_query(self, query, params=None):
        """
        Execute a SELECT query and return results.

        Args:
            query (str): SQL query
            params (tuple): Query parameters

        Returns:
            list: Query results
        """
        try:
            connection = self.get_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params or ())
                result = cursor.fetchall()
                cursor.close()
                return result
        except Exception as e:
            print(f"❌ Query error: {e}")
            return []

    def execute_update(self, query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query (str): SQL query
            params (tuple): Query parameters

        Returns:
            int: Last inserted ID or affected rows
        """
        global connection
        try:
            connection = self.get_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute(query, params or ())
                connection.commit()
                last_id = cursor.lastrowid
                affected = cursor.rowcount
                cursor.close()
                return last_id if last_id > 0 else affected
        except Exception as e:
            print(f"❌ Update error: {e}")
            connection.rollback()
            return 0

    @abstractmethod
    def find_by_id(self, entity_id):
        """Find entity by ID"""
        pass

    @abstractmethod
    def find_all(self):
        """Find all entities"""
        pass

    @abstractmethod
    def save(self, entity):
        """Save entity"""
        pass

    @abstractmethod
    def delete(self, entity_id):
        """Delete entity by ID"""
        pass