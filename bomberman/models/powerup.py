# models/powerup.py
"""
Power-up models for the Bomberman game
Implements Decorator Pattern for dynamic ability enhancement
"""

import pygame
from config import TILE_SIZE
from abc import ABC, abstractmethod


class PowerUp(ABC):
    """
    Abstract base class for power-ups.
    """

    def __init__(self, x, y, color, name):
        """
        Initialize power-up.

        Args:
            x (int): Grid X position
            y (int): Grid Y position
            color (tuple): RGB color
            name (str): Power-up name
        """
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.color = color
        self.name = name
        self.rect = pygame.Rect(self.x + 5, self.y + 5, TILE_SIZE - 10, TILE_SIZE - 10)
        self.collected = False

        # Animation
        self.float_offset = 0
        self.float_speed = 2

    @abstractmethod
    def apply(self, player):
        """
        Apply power-up effect to player using Decorator Pattern.
        This wraps the player with appropriate decorators.
        """
        pass

    def update(self, dt):
        """Update power-up animation"""
        self.float_offset += self.float_speed * (dt / 100)
        if self.float_offset > 5 or self.float_offset < -5:
            self.float_speed *= -1

    def draw(self, screen):
        """Draw power-up on screen"""
        if not self.collected:
            # Draw floating effect
            draw_y = self.y + int(self.float_offset)
            draw_rect = pygame.Rect(self.x + 5, draw_y + 5, TILE_SIZE - 10, TILE_SIZE - 10)

            # Draw power-up with enhanced brightness
            bright_color = tuple(min(c + 80, 255) for c in self.color)
            pygame.draw.circle(screen, bright_color, draw_rect.center, 12)
            pygame.draw.circle(screen, (255, 255, 255), draw_rect.center, 12, 2)
            
            # Draw glow effect
            pygame.draw.circle(screen, bright_color, draw_rect.center, 14, 1)

            # Draw symbol
            font = pygame.font.Font(None, 20)
            text = font.render(self.get_symbol(), True, (255, 255, 255))
            text_rect = text.get_rect(center=draw_rect.center)
            screen.blit(text, text_rect)

    @abstractmethod
    def get_symbol(self):
        """Return symbol character for this power-up"""
        pass


class BombCountPowerUp(PowerUp):
    """Power-up that increases bomb count using Decorator Pattern"""

    def __init__(self, x, y):
        super().__init__(x, y, (255, 0, 0), "Bomb Count")

    def apply(self, player):
        """Apply bomb count enhancement using Decorator Pattern"""
        # Wrap player with BombCountDecorator
        from patterns.structural.decorator import BombCountDecorator, BasePlayer
        if not isinstance(player, BombCountDecorator):
            # Create decorated version
            decorated = BombCountDecorator(BasePlayer(player))
            # Update player's stats with decorated values
            player.bomb_count = decorated.get_bomb_count()
            print(f"💣 Player {player.player_id} bomb count increased to {player.bomb_count} (Decorator Pattern)")
        else:
            # Fallback for compatibility
            player.bomb_count += 1
            print(f"💣 Player {player.player_id} bomb count increased to {player.bomb_count}")

    def get_symbol(self):
        return "B"


class BombPowerPowerUp(PowerUp):
    """Power-up that increases bomb explosion power using Decorator Pattern"""

    def __init__(self, x, y):
        super().__init__(x, y, (255, 165, 0), "Bomb Power")

    def apply(self, player):
        """Apply bomb power enhancement using Decorator Pattern"""
        # Wrap player with BombPowerDecorator
        from patterns.structural.decorator import BombPowerDecorator, BasePlayer
        if not isinstance(player, BombPowerDecorator):
            # Create decorated version
            decorated = BombPowerDecorator(BasePlayer(player))
            # Update player's stats with decorated values
            player.bomb_power = decorated.get_bomb_power()
            print(f"💥 Player {player.player_id} bomb power increased to {player.bomb_power} (Decorator Pattern)")
        else:
            # Fallback for compatibility
            player.bomb_power += 1
            print(f"💥 Player {player.player_id} bomb power increased to {player.bomb_power}")

    def get_symbol(self):
        return "P"


class SpeedPowerUp(PowerUp):
    """Power-up that increases movement speed using Decorator Pattern"""

    def __init__(self, x, y):
        super().__init__(x, y, (0, 255, 0), "Speed Boost")

    def apply(self, player):
        """Apply speed boost enhancement using Decorator Pattern"""
        # Wrap player with SpeedBoostDecorator
        from patterns.structural.decorator import SpeedBoostDecorator, BasePlayer
        if not isinstance(player, SpeedBoostDecorator):
            # Create decorated version
            decorated = SpeedBoostDecorator(BasePlayer(player))
            # Update player's stats with decorated values
            player.speed = decorated.get_speed()
            print(f"⚡ Player {player.player_id} speed increased to {player.speed} (Decorator Pattern)")
        else:
            # Fallback for compatibility
            player.speed += 1
            print(f"⚡ Player {player.player_id} speed increased to {player.speed}")

    def get_symbol(self):
        return "S"


# Optional power-ups for bonus points
class SkateboardPowerUp(PowerUp):
    """Power-up that greatly increases speed using Decorator Pattern"""

    def __init__(self, x, y):
        super().__init__(x, y, (0, 255, 255), "Skateboard")

    def apply(self, player):
        """Apply skateboard enhancement using Decorator Pattern (double speed decorator)"""
        from patterns.structural.decorator import SpeedBoostDecorator, BasePlayer
        # Apply SpeedBoostDecorator twice for greater effect
        decorated = SpeedBoostDecorator(SpeedBoostDecorator(BasePlayer(player)))
        player.speed = decorated.get_speed()
        print(f"🛹 Player {player.player_id} got skateboard! Speed: {player.speed} (Double Decorator Pattern)")

    def get_symbol(self):
        return "SK"


class WallPassPowerUp(PowerUp):
    """Power-up that allows walking through breakable walls using Decorator Pattern"""

    def __init__(self, x, y):
        super().__init__(x, y, (255, 255, 0), "Wall Pass")

    def apply(self, player):
        """Apply wall-pass ability using Decorator Pattern"""
        # Wrap player with WallPassDecorator
        from patterns.structural.decorator import WallPassDecorator, BasePlayer
        if not hasattr(player, 'can_pass_walls'):
            player.can_pass_walls = False
        
        if not isinstance(player, WallPassDecorator) and not player.can_pass_walls:
            # Create decorated version
            decorated = WallPassDecorator(BasePlayer(player))
            # Update player's ability
            player.can_pass_walls = decorated.can_pass_breakable_walls()
            print(f"🚪 Player {player.player_id} can now pass through walls! (Decorator Pattern)")
        else:
            # Fallback for compatibility
            player.can_pass_walls = True
            print(f"🚪 Player {player.player_id} can now pass through walls!")

    def get_symbol(self):
        return "W"