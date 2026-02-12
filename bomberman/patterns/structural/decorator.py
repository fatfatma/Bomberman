# patterns/structural/decorator.py
"""
Decorator Pattern - Player Ability Enhancement
Dynamically adds abilities to players without modifying their base class
"""

from abc import ABC, abstractmethod


class PlayerComponent(ABC):
    """
    Abstract component for player abilities.
    This is the base interface that both Player and decorators will implement.
    """

    @abstractmethod
    def get_speed(self):
        """Get player speed"""
        pass

    @abstractmethod
    def get_bomb_count(self):
        """Get max bomb count"""
        pass

    @abstractmethod
    def get_bomb_power(self):
        """Get bomb explosion power"""
        pass

    @abstractmethod
    def can_pass_breakable_walls(self):
        """Check if can pass through breakable walls"""
        pass


class BasePlayer(PlayerComponent):
    """
    Concrete component - wraps the actual Player object.
    This allows us to decorate the player with abilities.
    """

    def __init__(self, player):
        self.player = player

    def get_speed(self):
        return self.player.speed

    def get_bomb_count(self):
        return self.player.bomb_count

    def get_bomb_power(self):
        return self.player.bomb_power

    def can_pass_breakable_walls(self):
        return getattr(self.player, 'can_pass_walls', False)


class PlayerDecorator(PlayerComponent):
    """
    Abstract decorator class.
    Wraps a PlayerComponent and delegates calls to it.
    """

    def __init__(self, player_component):
        self._player_component = player_component

    def get_speed(self):
        return self._player_component.get_speed()

    def get_bomb_count(self):
        return self._player_component.get_bomb_count()

    def get_bomb_power(self):
        return self._player_component.get_bomb_power()

    def can_pass_breakable_walls(self):
        return self._player_component.can_pass_breakable_walls()


class SpeedBoostDecorator(PlayerDecorator):
    """
    Concrete decorator that adds speed boost.
    """

    def __init__(self, player_component, boost_amount=1):
        super().__init__(player_component)
        self.boost_amount = boost_amount

    def get_speed(self):
        """Add speed boost to base speed"""
        return self._player_component.get_speed() + self.boost_amount


class BombCountDecorator(PlayerDecorator):
    """
    Concrete decorator that increases bomb count.
    """

    def __init__(self, player_component, extra_bombs=1):
        super().__init__(player_component)
        self.extra_bombs = extra_bombs

    def get_bomb_count(self):
        """Add extra bombs to base count"""
        return self._player_component.get_bomb_count() + self.extra_bombs


class BombPowerDecorator(PlayerDecorator):
    """
    Concrete decorator that increases bomb power.
    """

    def __init__(self, player_component, extra_power=1):
        super().__init__(player_component)
        self.extra_power = extra_power

    def get_bomb_power(self):
        """Add extra power to base power"""
        return self._player_component.get_bomb_power() + self.extra_power


class WallPassDecorator(PlayerDecorator):
    """
    Concrete decorator that allows passing through breakable walls.
    """

    def can_pass_breakable_walls(self):
        """Enable wall passing"""
        return True


class PlayerEnhancer:
    """
    Utility class to apply decorators to players.
    This makes it easier to stack multiple abilities.
    """

    @staticmethod
    def enhance_player(player, enhancements):
        """
        Apply multiple enhancements to a player.

        Args:
            player: Player object to enhance
            enhancements (list): List of enhancement types

        Returns:
            PlayerComponent: Decorated player component

        Example:
            enhanced = PlayerEnhancer.enhance_player(player, ['speed', 'bomb_count', 'wall_pass'])
        """
        component = BasePlayer(player)

        for enhancement in enhancements:
            if enhancement == 'speed':
                component = SpeedBoostDecorator(component)
            elif enhancement == 'bomb_count':
                component = BombCountDecorator(component)
            elif enhancement == 'bomb_power':
                component = BombPowerDecorator(component)
            elif enhancement == 'wall_pass':
                component = WallPassDecorator(component)

        return component


# Usage example and test
if __name__ == "__main__":
    from models.player import Player
    import pygame

    print("=== Testing Decorator Pattern ===\n")

    # Create a base player
    player = Player(1, 1, 1, (255, 0, 0), {})
    print(f"Base Player Stats:")
    print(f"  Speed: {player.speed}")
    print(f"  Bomb Count: {player.bomb_count}")
    print(f"  Bomb Power: {player.bomb_power}")
    print(f"  Can Pass Walls: {getattr(player, 'can_pass_walls', False)}")

    # Apply decorators
    print(f"\n--- Applying Decorators ---")
    enhanced = PlayerEnhancer.enhance_player(
        player,
        ['speed', 'speed', 'bomb_count', 'bomb_power', 'wall_pass']
    )

    print(f"\nEnhanced Player Stats:")
    print(f"  Speed: {enhanced.get_speed()} (+{enhanced.get_speed() - player.speed})")
    print(f"  Bomb Count: {enhanced.get_bomb_count()} (+{enhanced.get_bomb_count() - player.bomb_count})")
    print(f"  Bomb Power: {enhanced.get_bomb_power()} (+{enhanced.get_bomb_power() - player.bomb_power})")
    print(f"  Can Pass Walls: {enhanced.can_pass_breakable_walls()}")

    print("\n✅ Decorator Pattern test completed!")