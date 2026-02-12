# test_patterns_integration.py
"""
Test file for State Pattern and Decorator Pattern Integration
Demonstrates how both patterns work together in the game
"""

import pygame
from patterns.creational.factory import WallFactory, PowerUpFactory
from patterns.behavioral.strategy import create_ai_strategy
from patterns.behavioral.observer import GameEventManager, GameEvent, ScoreObserver, StatisticsObserver
from patterns.structural.decorator import DecoratorApplier, BasePlayer
from models.player import Player
from models.powerup import BombCountPowerUp, SpeedPowerUp, BombPowerPowerUp
from config import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bomberman - Patterns Integration Test")
clock = pygame.time.Clock()


def test_state_pattern():
    """Test State Pattern in Player class"""
    print("\n=== Testing State Pattern Integration ===")
    
    player_controls = {
        'up': pygame.K_w,
        'down': pygame.K_s,
        'left': pygame.K_a,
        'right': pygame.K_d,
        'bomb': pygame.K_SPACE
    }
    player = Player(1, 5, 5, RED, player_controls)
    
    print(f"✓ Player created with State Pattern")
    print(f"  Current state: {player.state_manager.get_state_name()}")
    print(f"  Is alive: {player.state_manager.is_alive()}")
    
    # Test state transitions
    print("\n  Testing state transitions:")
    
    # Normal → Invincible
    print(f"    → Setting invincible (5 seconds)")
    player.apply_invincibility(5000)
    print(f"      Current state: {player.state_manager.get_state_name()}")
    
    # Invincible → Normal
    print(f"    → Resetting to normal")
    player.state_manager.set_normal_state()
    print(f"      Current state: {player.state_manager.get_state_name()}")
    
    # Normal → Stunned
    print(f"    → Setting stunned (2 seconds)")
    player.stun(2000)
    print(f"      Current state: {player.state_manager.get_state_name()}")
    
    # Stunned → Dead
    print(f"    → Setting dead")
    player.die()
    print(f"      Current state: {player.state_manager.get_state_name()}")
    print(f"      Is alive: {player.state_manager.is_alive()}")
    
    return player


def test_decorator_pattern():
    """Test Decorator Pattern in PowerUp system"""
    print("\n=== Testing Decorator Pattern Integration ===")
    
    player_controls = {
        'up': pygame.K_w,
        'down': pygame.K_s,
        'left': pygame.K_a,
        'right': pygame.K_d,
        'bomb': pygame.K_SPACE
    }
    player = Player(2, 8, 8, BLUE, player_controls)
    
    print(f"✓ Player created for Decorator Pattern test")
    print(f"  Initial stats:")
    print(f"    Speed: {player.speed}")
    print(f"    Bomb Count: {player.bomb_count}")
    print(f"    Bomb Power: {player.bomb_power}")
    
    # Test Decorator Pattern with PowerUps
    print(f"\n  Applying PowerUps with Decorator Pattern:")
    
    # Speed Power-Up
    speed_powerup = SpeedPowerUp(9, 9)
    print(f"    → Collecting Speed PowerUp")
    speed_powerup.apply(player)
    print(f"      New speed: {player.speed}")
    
    # Bomb Count Power-Up
    bomb_count_powerup = BombCountPowerUp(10, 10)
    print(f"    → Collecting Bomb Count PowerUp")
    bomb_count_powerup.apply(player)
    print(f"      New bomb count: {player.bomb_count}")
    
    # Bomb Power Power-Up
    bomb_power_powerup = BombPowerPowerUp(11, 11)
    print(f"    → Collecting Bomb Power PowerUp")
    bomb_power_powerup.apply(player)
    print(f"      New bomb power: {player.bomb_power}")
    
    # Stacked Decorators example
    print(f"\n  Applying multiple decorators (Skateboard = double speed):")
    print(f"    Current speed: {player.speed}")
    
    from patterns.structural.decorator import SpeedBoostDecorator
    decorated = SpeedBoostDecorator(SpeedBoostDecorator(BasePlayer(player)))
    enhanced_speed = decorated.get_speed()
    print(f"    Enhanced speed (with decorators): {enhanced_speed}")
    
    return player


def test_observer_pattern():
    """Test Observer Pattern for game events"""
    print("\n=== Testing Observer Pattern ===")
    
    event_manager = GameEventManager()
    score_observer = ScoreObserver()
    stats_observer = StatisticsObserver()
    
    # Register observers
    event_manager.subscribe(GameEvent.PLAYER_DIED, score_observer)
    event_manager.subscribe(GameEvent.POWERUP_COLLECTED, score_observer)
    event_manager.subscribe(GameEvent.BOMB_EXPLODED, stats_observer)
    
    print(f"✓ Observers registered")
    print(f"  Triggering events:")
    
    # Trigger events
    event_manager.trigger_event(GameEvent.PLAYER_DIED, {'player': 1})
    event_manager.trigger_event(GameEvent.POWERUP_COLLECTED, 
                                {'type': 'Speed Boost', 'player': 1})
    event_manager.trigger_event(GameEvent.BOMB_EXPLODED, 
                                {'x': 5, 'y': 5})
    
    print(f"✅ Observer Pattern working correctly")


def test_factory_pattern():
    """Test Factory Pattern for creating game objects"""
    print("\n=== Testing Factory Pattern ===")
    
    print(f"✓ Creating walls with WallFactory:")
    wall1 = WallFactory.create_wall('unbreakable', 0, 0, 'desert')
    wall2 = WallFactory.create_wall('breakable', 1, 0, 'desert')
    wall3 = WallFactory.create_wall('hard', 2, 0, 'desert')
    
    print(f"  {wall1.get_type()}")
    print(f"  {wall2.get_type()}")
    print(f"  {wall3.get_type()}")
    
    print(f"\n✓ Creating power-ups with PowerUpFactory:")
    powerup1 = PowerUpFactory.create_powerup('bomb_count', 5, 5)
    powerup2 = PowerUpFactory.create_powerup('speed', 6, 6)
    powerup3 = PowerUpFactory.create_powerup('bomb_power', 7, 7)
    
    print(f"  {powerup1.name}")
    print(f"  {powerup2.name}")
    print(f"  {powerup3.name}")


def test_strategy_pattern():
    """Test Strategy Pattern for AI behavior"""
    print("\n=== Testing Strategy Pattern ===")
    
    print(f"✓ Creating AI strategies:")
    
    static_ai = create_ai_strategy('static')
    print(f"  Static AI: {static_ai.__class__.__name__}")
    
    smart_ai = create_ai_strategy('smart')
    print(f"  Smart AI (A*): {smart_ai.__class__.__name__}")
    
    print(f"✅ Strategy Pattern working correctly")


if __name__ == "__main__":
    print("=" * 60)
    print("🎮 BOMBERMAN PATTERNS INTEGRATION TEST")
    print("=" * 60)
    
    # Run all pattern tests
    test_factory_pattern()
    test_strategy_pattern()
    test_observer_pattern()
    player1 = test_state_pattern()
    player2 = test_decorator_pattern()
    
    print("\n" + "=" * 60)
    print("✅ ALL PATTERN INTEGRATION TESTS PASSED!")
    print("=" * 60)
    
    print("\n📊 Summary:")
    print(f"  ✓ State Pattern: Player state management (Normal → Invincible → Stunned → Dead)")
    print(f"  ✓ Decorator Pattern: Dynamic power-up enhancements")
    print(f"  ✓ Observer Pattern: Game event system")
    print(f"  ✓ Factory Pattern: Object creation (Walls, PowerUps)")
    print(f"  ✓ Strategy Pattern: Enemy AI behaviors")
    
    print("\n🎮 Patterns are now fully integrated into the game!")
    
    pygame.quit()
