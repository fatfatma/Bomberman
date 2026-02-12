# database/user_repository.py
"""
User Repository - Handles all user-related database operations
"""

import hashlib
from database.repository import Repository


class User:
    """User entity class"""

    def __init__(self, user_id=None, username=None, password_hash=None, created_at=None):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at

    def __repr__(self):
        return f"User(id={self.user_id}, username='{self.username}')"


class UserRepository(Repository):
    """
    Repository for User operations.
    Implements CRUD operations for users.
    """

    def find_by_id(self, user_id):
        """
        Find user by ID.

        Args:
            user_id (int): User ID

        Returns:
            User: User object or None
        """
        query = "SELECT * FROM users WHERE user_id = %s"
        results = self.execute_query(query, (user_id,))

        if results:
            row = results[0]
            return User(
                user_id=row['user_id'],
                username=row['username'],
                password_hash=row['password_hash'],
                created_at=row['created_at']
            )
        return None

    def find_by_username(self, username):
        """
        Find user by username.

        Args:
            username (str): Username

        Returns:
            User: User object or None
        """
        query = "SELECT * FROM users WHERE username = %s"
        results = self.execute_query(query, (username,))

        if results:
            row = results[0]
            return User(
                user_id=row['user_id'],
                username=row['username'],
                password_hash=row['password_hash'],
                created_at=row['created_at']
            )
        return None

    def find_all(self):
        """
        Get all users.

        Returns:
            list: List of User objects
        """
        query = "SELECT * FROM users"
        results = self.execute_query(query)

        users = []
        for row in results:
            users.append(User(
                user_id=row['user_id'],
                username=row['username'],
                password_hash=row['password_hash'],
                created_at=row['created_at']
            ))
        return users

    def save(self, user):
        """
        Create a new user.

        Args:
            user (User): User object

        Returns:
            int: New user ID
        """
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        user_id = self.execute_update(query, (user.username, user.password_hash))

        if user_id:
            user.user_id = user_id
            print(f"✅ User created: {user.username} (ID: {user_id})")

            # Also create default entries in related tables
            self._create_default_stats(user_id)
            self._create_default_preferences(user_id)

        return user_id

    def update(self, user):
        """
        Update existing user.

        Args:
            user (User): User object with updated data

        Returns:
            bool: True if successful
        """
        query = "UPDATE users SET username = %s, password_hash = %s WHERE user_id = %s"
        affected = self.execute_update(query, (user.username, user.password_hash, user.user_id))
        return affected > 0

    def delete(self, user_id):
        """
        Delete user by ID.

        Args:
            user_id (int): User ID

        Returns:
            bool: True if successful
        """
        query = "DELETE FROM users WHERE user_id = %s"
        affected = self.execute_update(query, (user_id,))

        if affected:
            print(f"✅ User deleted (ID: {user_id})")
        return affected > 0

    def authenticate(self, username, password):
        """
        Authenticate user with username and password.

        Args:
            username (str): Username
            password (str): Plain text password

        Returns:
            User: User object if authenticated, None otherwise
        """
        user = self.find_by_username(username)

        if user:
            password_hash = self._hash_password(password)
            if user.password_hash == password_hash:
                print(f"✅ User authenticated: {username}")
                return user
            else:
                print(f"❌ Invalid password for user: {username}")
        else:
            print(f"❌ User not found: {username}")

        return None

    def register(self, username, password):
        """
        Register a new user.

        Args:
            username (str): Username
            password (str): Plain text password

        Returns:
            User: New user object or None if username exists
        """
        # Check if username already exists
        existing_user = self.find_by_username(username)
        if existing_user:
            print(f"❌ Username already exists: {username}")
            return None

        # Create new user
        password_hash = self._hash_password(password)
        user = User(username=username, password_hash=password_hash)
        self.save(user)

        return user

    def _hash_password(self, password):
        """
        Hash password using SHA-256.

        Args:
            password (str): Plain text password

        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _create_default_stats(self, user_id):
        """Create default stats for new user"""
        query = "INSERT INTO game_stats (user_id) VALUES (%s)"
        self.execute_update(query, (user_id,))

    def _create_default_preferences(self, user_id):
        """Create default preferences for new user"""
        query = "INSERT INTO user_preferences (user_id, theme) VALUES (%s, 'desert')"
        self.execute_update(query, (user_id,))


# Usage Example
if __name__ == "__main__":
    print("=== Testing User Repository ===\n")

    repo = UserRepository()

    # Test registration
    print("--- Testing Registration ---")
    user1 = repo.register("player1", "password123")
    user2 = repo.register("player2", "password456")

    # Test duplicate username
    duplicate = repo.register("player1", "different_pass")

    # Test authentication
    print("\n--- Testing Authentication ---")
    auth_user = repo.authenticate("player1", "password123")
    failed_auth = repo.authenticate("player1", "wrong_password")

    # Test find operations
    print("\n--- Testing Find Operations ---")
    found_user = repo.find_by_username("player1")
    print(f"Found user: {found_user}")

    all_users = repo.find_all()
    print(f"Total users: {len(all_users)}")
    for user in all_users:
        print(f"  - {user}")

    print("\n✅ User Repository test completed!")