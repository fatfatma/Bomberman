# database/game_repository.py
"""
Game Repository - Handles game statistics and leaderboard operations
"""

from database.repository import Repository


class GameStats:
    """Game statistics entity"""

    def __init__(self, stat_id=None, user_id=None, wins=0, losses=0, total_games=0):
        self.stat_id = stat_id
        self.user_id = user_id
        self.wins = wins
        self.losses = losses
        self.total_games = total_games

    def __repr__(self):
        return f"GameStats(user_id={self.user_id}, W:{self.wins} L:{self.losses} T:{self.total_games})"


class LeaderboardEntry:
    """Leaderboard entry entity"""

    def __init__(self, score_id=None, user_id=None, username=None, score=0, game_date=None):
        self.score_id = score_id
        self.user_id = user_id
        self.username = username
        self.score = score
        self.game_date = game_date

    def __repr__(self):
        return f"LeaderboardEntry({self.username}: {self.score} pts)"


class UserPreferences:
    """User preferences entity"""

    def __init__(self, pref_id=None, user_id=None, theme='desert'):
        self.pref_id = pref_id
        self.user_id = user_id
        self.theme = theme

    def __repr__(self):
        return f"UserPreferences(user_id={self.user_id}, theme='{self.theme}')"


class GameRepository(Repository):
    """
    Repository for game-related operations.
    Handles stats, leaderboard, and preferences.
    """

    # Game Stats Methods

    def find_by_id(self, stat_id):
        """Find stats by ID"""
        query = "SELECT * FROM game_stats WHERE stat_id = %s"
        results = self.execute_query(query, (stat_id,))

        if results:
            row = results[0]
            return GameStats(
                stat_id=row['stat_id'],
                user_id=row['user_id'],
                wins=row['wins'],
                losses=row['losses'],
                total_games=row['total_games']
            )
        return None

    def find_stats_by_user(self, user_id):
        """
        Get game stats for a specific user.

        Args:
            user_id (int): User ID

        Returns:
            GameStats: Stats object or None
        """
        query = "SELECT * FROM game_stats WHERE user_id = %s"
        results = self.execute_query(query, (user_id,))

        if results:
            row = results[0]
            return GameStats(
                stat_id=row['stat_id'],
                user_id=row['user_id'],
                wins=row['wins'],
                losses=row['losses'],
                total_games=row['total_games']
            )
        return None

    def find_all(self):
        """Get all game stats"""
        query = "SELECT * FROM game_stats"
        results = self.execute_query(query)

        stats_list = []
        for row in results:
            stats_list.append(GameStats(
                stat_id=row['stat_id'],
                user_id=row['user_id'],
                wins=row['wins'],
                losses=row['losses'],
                total_games=row['total_games']
            ))
        return stats_list

    def save(self, stats):
        """Save new game stats"""
        query = "INSERT INTO game_stats (user_id, wins, losses, total_games) VALUES (%s, %s, %s, %s)"
        stat_id = self.execute_update(query, (stats.user_id, stats.wins, stats.losses, stats.total_games))
        stats.stat_id = stat_id
        return stat_id

    def update_stats(self, user_id, won):
        """
        Update game statistics after a match.

        Args:
            user_id (int): User ID
            won (bool): True if player won, False if lost

        Returns:
            bool: True if successful
        """
        if won:
            query = """
                UPDATE game_stats 
                SET wins = wins + 1, total_games = total_games + 1 
                WHERE user_id = %s
            """
        else:
            query = """
                UPDATE game_stats 
                SET losses = losses + 1, total_games = total_games + 1 
                WHERE user_id = %s
            """

        affected = self.execute_update(query, (user_id,))
        if affected:
            result = "won" if won else "lost"
            print(f"✅ Stats updated: User {user_id} {result}")
        return affected > 0

    def delete(self, stat_id):
        """Delete game stats"""
        query = "DELETE FROM game_stats WHERE stat_id = %s"
        return self.execute_update(query, (stat_id,)) > 0

    # Leaderboard Methods

    def add_score(self, user_id, score):
        """
        Add a score to the leaderboard.

        Args:
            user_id (int): User ID
            score (int): Score to add

        Returns:
            int: Score ID
        """
        query = "INSERT INTO leaderboard (user_id, score) VALUES (%s, %s)"
        score_id = self.execute_update(query, (user_id, score))

        if score_id:
            print(f"✅ Score added: User {user_id} scored {score}")
        return score_id

    def get_leaderboard(self, limit=10):
        """
        Get top scores from leaderboard.

        Args:
            limit (int): Number of entries to return

        Returns:
            list: List of LeaderboardEntry objects
        """
        query = """
            SELECT l.score_id, l.user_id, u.username, l.score, l.game_date
            FROM leaderboard l
            JOIN users u ON l.user_id = u.user_id
            ORDER BY l.score DESC
            LIMIT %s
        """
        results = self.execute_query(query, (limit,))

        leaderboard = []
        for row in results:
            leaderboard.append(LeaderboardEntry(
                score_id=row['score_id'],
                user_id=row['user_id'],
                username=row['username'],
                score=row['score'],
                game_date=row['game_date']
            ))
        return leaderboard

    def get_user_best_score(self, user_id):
        """
        Get user's best score.

        Args:
            user_id (int): User ID

        Returns:
            int: Best score or 0
        """
        query = "SELECT MAX(score) as best_score FROM leaderboard WHERE user_id = %s"
        results = self.execute_query(query, (user_id,))

        if results and results[0]['best_score']:
            return results[0]['best_score']
        return 0

    # User Preferences Methods

    def get_preferences(self, user_id):
        """
        Get user preferences.

        Args:
            user_id (int): User ID

        Returns:
            UserPreferences: Preferences object or None
        """
        query = "SELECT * FROM user_preferences WHERE user_id = %s"
        results = self.execute_query(query, (user_id,))

        if results:
            row = results[0]
            return UserPreferences(
                pref_id=row['pref_id'],
                user_id=row['user_id'],
                theme=row['theme']
            )
        return None

    def update_theme(self, user_id, theme):
        """
        Update user's theme preference.

        Args:
            user_id (int): User ID
            theme (str): Theme name ('desert', 'forest', 'city')

        Returns:
            bool: True if successful
        """
        query = "UPDATE user_preferences SET theme = %s WHERE user_id = %s"
        affected = self.execute_update(query, (theme, user_id))

        if affected:
            print(f"✅ Theme updated: User {user_id} → {theme}")
        return affected > 0


# Usage Example
if __name__ == "__main__":
    print("=== Testing Game Repository ===\n")

    from database.user_repository import UserRepository

    # Create test user
    user_repo = UserRepository()
    test_user = user_repo.register("test_player", "test123")

    if test_user:
        game_repo = GameRepository()

        # Test stats
        print("--- Testing Game Stats ---")
        stats = game_repo.find_stats_by_user(test_user.user_id)
        print(f"Initial stats: {stats}")

        # Simulate some games
        game_repo.update_stats(test_user.user_id, won=True)
        game_repo.update_stats(test_user.user_id, won=True)
        game_repo.update_stats(test_user.user_id, won=False)

        stats = game_repo.find_stats_by_user(test_user.user_id)
        print(f"Updated stats: {stats}")

        # Test leaderboard
        print("\n--- Testing Leaderboard ---")
        game_repo.add_score(test_user.user_id, 1500)
        game_repo.add_score(test_user.user_id, 2000)
        game_repo.add_score(test_user.user_id, 1800)

        leaderboard = game_repo.get_leaderboard(5)
        print("Top Scores:")
        for i, entry in enumerate(leaderboard, 1):
            print(f"  {i}. {entry}")

        best = game_repo.get_user_best_score(test_user.user_id)
        print(f"Best score: {best}")

        # Test preferences
        print("\n--- Testing Preferences ---")
        prefs = game_repo.get_preferences(test_user.user_id)
        print(f"Current preferences: {prefs}")

        game_repo.update_theme(test_user.user_id, 'forest')
        prefs = game_repo.get_preferences(test_user.user_id)
        print(f"Updated preferences: {prefs}")

    print("\n✅ Game Repository test completed!")