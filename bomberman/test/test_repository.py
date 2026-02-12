# test_repository.py
"""
Test Repository Pattern with database operations
"""

from database.user_repository import UserRepository
from database.game_repository import GameRepository

print("=" * 60)
print("REPOSITORY PATTERN TEST")
print("=" * 60)

# Initialize repositories
user_repo = UserRepository()
game_repo = GameRepository()

print("\n--- Part 1: User Management ---")

# Register new users
print("\n1. Registering users...")
user1 = user_repo.register("bomberman_pro", "securepass123")
user2 = user_repo.register("noob_player", "password456")

# Try duplicate username
print("\n2. Testing duplicate username...")
duplicate = user_repo.register("bomberman_pro", "different_pass")

# Authenticate users
print("\n3. Testing authentication...")
auth_success = user_repo.authenticate("bomberman_pro", "securepass123")
auth_fail = user_repo.authenticate("bomberman_pro", "wrong_password")
auth_notfound = user_repo.authenticate("nonexistent", "pass")

# List all users
print("\n4. All users in database:")
all_users = user_repo.find_all()
for user in all_users:
    print(f"   {user}")

print("\n--- Part 2: Game Statistics ---")

if user1 and user2:
    # Get initial stats
    print("\n5. Initial game stats:")
    stats1 = game_repo.find_stats_by_user(user1.user_id)
    stats2 = game_repo.find_stats_by_user(user2.user_id)
    print(f"   User1: {stats1}")
    print(f"   User2: {stats2}")

    # Simulate some games
    print("\n6. Simulating game results...")
    print("   User1 wins 3 games, loses 1")
    game_repo.update_stats(user1.user_id, won=True)
    game_repo.update_stats(user1.user_id, won=True)
    game_repo.update_stats(user1.user_id, won=True)
    game_repo.update_stats(user1.user_id, won=False)

    print("   User2 wins 1 game, loses 2")
    game_repo.update_stats(user2.user_id, won=True)
    game_repo.update_stats(user2.user_id, won=False)
    game_repo.update_stats(user2.user_id, won=False)

    # Check updated stats
    print("\n7. Updated game stats:")
    stats1 = game_repo.find_stats_by_user(user1.user_id)
    stats2 = game_repo.find_stats_by_user(user2.user_id)
    print(f"   User1: {stats1}")
    print(f"   User2: {stats2}")

print("\n--- Part 3: Leaderboard ---")

if user1 and user2:
    # Add scores
    print("\n8. Adding scores to leaderboard...")
    game_repo.add_score(user1.user_id, 2500)
    game_repo.add_score(user1.user_id, 1800)
    game_repo.add_score(user1.user_id, 3200)
    game_repo.add_score(user2.user_id, 1500)
    game_repo.add_score(user2.user_id, 2100)

    # Get leaderboard
    print("\n9. Top 10 Leaderboard:")
    leaderboard = game_repo.get_leaderboard(10)
    for i, entry in enumerate(leaderboard, 1):
        print(f"   #{i} {entry.username}: {entry.score} pts (ID: {entry.user_id})")

    # Get best scores
    print("\n10. Best scores:")
    best1 = game_repo.get_user_best_score(user1.user_id)
    best2 = game_repo.get_user_best_score(user2.user_id)
    print(f"   User1 best: {best1}")
    print(f"   User2 best: {best2}")

print("\n--- Part 4: User Preferences ---")

if user1 and user2:
    # Get preferences
    print("\n11. Current preferences:")
    prefs1 = game_repo.get_preferences(user1.user_id)
    prefs2 = game_repo.get_preferences(user2.user_id)
    print(f"   User1: {prefs1}")
    print(f"   User2: {prefs2}")

    # Update themes
    print("\n12. Updating themes...")
    game_repo.update_theme(user1.user_id, 'forest')
    game_repo.update_theme(user2.user_id, 'city')

    # Check updated preferences
    print("\n13. Updated preferences:")
    prefs1 = game_repo.get_preferences(user1.user_id)
    prefs2 = game_repo.get_preferences(user2.user_id)
    print(f"   User1: {prefs1}")
    print(f"   User2: {prefs2}")

print("\n" + "=" * 60)
print("✅ REPOSITORY PATTERN TEST COMPLETED!")
print("=" * 60)

print("\nRepository Pattern Summary:")
print("  ✓ User Repository - Registration, Authentication, CRUD")
print("  ✓ Game Repository - Stats tracking, Leaderboard, Preferences")
print("  ✓ Singleton Pattern - Single database connection")
print("  ✓ Clean abstraction - Business logic separated from SQL")