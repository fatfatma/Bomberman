# models/wall.py
"""
Wall models for the game
Three types: Unbreakable, Breakable, Hard
"""

import pygame
from abc import ABC, abstractmethod
from config import TILE_SIZE


class Wall(ABC):
    """
    Abstract base class for all wall types.
    Implements common wall functionality.
    """

    def __init__(self, x, y, color):
        self.grid_x = x  # Grid position
        self.grid_y = y  # Grid position
        self.x = x * TILE_SIZE  # Pixel position
        self.y = y * TILE_SIZE  # Pixel position
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        self.destroyed = False

    @abstractmethod
    def take_damage(self):
        """
        Abstract method to handle damage.
        Each wall type implements this differently.
        """
        pass

    @abstractmethod
    def get_type(self):
        """Return the wall type as string"""
        pass

    def draw(self, screen):
        """Draw the wall on screen"""
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border


class UnbreakableWall(Wall):
    """
    Unbreakable wall - Cannot be destroyed.
    Used for map boundaries and permanent obstacles.
    """

    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def take_damage(self):
        """Unbreakable walls take no damage"""
        return False

    def get_type(self):
        return "unbreakable"


class BreakableWall(Wall):
    """
    Breakable wall - Destroyed with a single explosion.
    May drop power-ups when destroyed.
    """

    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def take_damage(self):
        """Destroy wall on first hit"""
        self.destroyed = True
        return True

    def get_type(self):
        return "breakable"


class HardWall(Wall):
    """
    Hard wall - Requires multiple explosions to destroy.
    Shows damage progression.
    """

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.max_health = 3
        self.health = self.max_health
        self.original_color = color

    def take_damage(self):
        """Reduce health, destroy when health reaches 0"""
        if self.health > 0:
            self.health -= 1
            # Change color to show damage
            darker_factor = self.health / self.max_health
            self.color = tuple(int(c * darker_factor) for c in self.original_color)

            if self.health <= 0:
                self.destroyed = True
                return True
        return False

    def get_type(self):
        return "hard"

    def draw(self, screen):
        """Override draw to show health bar"""
        if not self.destroyed:
            # Draw wall
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

            # Draw health bar
            if self.health < self.max_health:
                health_bar_width = (self.health / self.max_health) * TILE_SIZE
                health_bar_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y - 5,
                    health_bar_width,
                    3
                )
                pygame.draw.rect(screen, (255, 0, 0), health_bar_rect)