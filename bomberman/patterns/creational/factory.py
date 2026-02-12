# patterns/creational/factory.py
"""
Factory Method Pattern - Wall Factory
Creates different types of walls without exposing creation logic
"""

from models.wall import UnbreakableWall, BreakableWall, HardWall
from config import THEMES


class WallFactory:
    """
    Factory class for creating wall objects.
    Encapsulates the creation logic for different wall types.
    """

    @staticmethod
    def create_wall(wall_type, x, y, theme='desert'):
        """
        Factory method to create walls based on type.

        Args:
            wall_type (str): Type of wall ('unbreakable', 'breakable', 'hard')
            x (int): X grid position
            y (int): Y grid position
            theme (str): Theme name for color selection

        Returns:
            Wall: Appropriate wall object
        """
        theme_colors = THEMES.get(theme, THEMES['desert'])

        if wall_type == 'unbreakable':
            return UnbreakableWall(x, y, theme_colors['unbreakable_color'])
        elif wall_type == 'breakable':
            return BreakableWall(x, y, theme_colors['breakable_color'])
        elif wall_type == 'hard':
            return HardWall(x, y, theme_colors['hard_color'])
        else:
            raise ValueError(f"Unknown wall type: {wall_type}")


class PowerUpFactory:
    """
    Factory class for creating power-up objects.
    """

    @staticmethod
    def create_powerup(powerup_type, x, y):
        """
        Factory method to create power-ups.

        Args:
            powerup_type (str): Type of power-up
            x (int): X position
            y (int): Y position

        Returns:
            PowerUp: Appropriate power-up object
        """
        from models.powerup import (BombCountPowerUp, BombPowerPowerUp,
                                    SpeedPowerUp, SkateboardPowerUp, WallPassPowerUp)

        if powerup_type == 'bomb_count':
            return BombCountPowerUp(x, y)
        elif powerup_type == 'bomb_power':
            return BombPowerPowerUp(x, y)
        elif powerup_type == 'speed_boost':
            return SpeedPowerUp(x, y)
        elif powerup_type == 'skateboard':
            return SkateboardPowerUp(x, y)
        elif powerup_type == 'wall_pass':
            return WallPassPowerUp(x, y)
        else:
            raise ValueError(f"Unknown power-up type: {powerup_type}")


# Usage Example and Test
if __name__ == "__main__":
    import pygame

    pygame.init()

    # Test wall creation
    print("=== Testing Wall Factory ===")

    # Create different wall types
    unbreakable = WallFactory.create_wall('unbreakable', 0, 0, 'desert')
    breakable = WallFactory.create_wall('breakable', 1, 0, 'forest')
    hard = WallFactory.create_wall('hard', 2, 0, 'city')

    print(f"Created {unbreakable.get_type()} wall at (0,0)")
    print(f"Created {breakable.get_type()} wall at (1,0)")
    print(f"Created {hard.get_type()} wall at (2,0)")

    # Test damage
    print("\n=== Testing Damage System ===")
    print(f"Unbreakable wall destroyed: {unbreakable.take_damage()}")
    print(f"Breakable wall destroyed: {breakable.take_damage()}")
    print(f"Hard wall hit 1: {hard.take_damage()}")
    print(f"Hard wall hit 2: {hard.take_damage()}")
    print(f"Hard wall hit 3: {hard.take_damage()}")

    print("\n✅ Factory Pattern test completed!")