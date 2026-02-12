# models/bomb.py
"""
Bomb model for the Bomberman game
"""

import pygame
from config import TILE_SIZE, BOMB_TIMER


class Bomb:
    """
    Bomb class that explodes after a timer.
    Explosion propagates in 4 directions.
    """

    def __init__(self, x, y, power, owner):
        """
        Initialize bomb.

        Args:
            x (int): Grid X position
            y (int): Grid Y position
            power (int): Explosion range in tiles
            owner (Player): Player who placed the bomb
        """
        self.grid_x = x
        self.grid_y = y
        self.power = power
        self.owner = owner

        # Pixel position for drawing
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

        # Timer
        self.timer = BOMB_TIMER
        self.exploded = False

        # Animation
        self.blink_timer = 0
        self.blink_visible = True

    def update(self, dt):
        """
        Update bomb timer.

        Args:
            dt (int): Delta time in milliseconds

        Returns:
            bool: True if bomb should explode
        """
        if self.exploded:
            return False

        self.timer -= dt

        # Blinking animation
        self.blink_timer += dt
        if self.blink_timer > 200:  # Blink every 200ms
            self.blink_visible = not self.blink_visible
            self.blink_timer = 0

        if self.timer <= 0:
            self.exploded = True
            return True

        return False

    def draw(self, screen):
        """Draw the bomb on screen"""
        if not self.exploded and self.blink_visible:
            try:
                from assets.asset_loader import get_asset_loader
                loader = get_asset_loader()
                sprite = loader.get_image('bomb')

                if sprite:
                    screen.blit(sprite, (self.rect.x, self.rect.y))

                    # Draw fuse on top
                    fuse_length = int((self.timer / BOMB_TIMER) * 10)
                    if fuse_length > 0:
                        pygame.draw.line(screen, (255, 100, 0),
                                         (self.rect.centerx, self.rect.centery - TILE_SIZE // 3),
                                         (self.rect.centerx, self.rect.centery - TILE_SIZE // 3 - fuse_length),
                                         2)
                        # Spark
                        pygame.draw.circle(screen, (255, 200, 0),
                                           (self.rect.centerx, self.rect.centery - TILE_SIZE // 3 - fuse_length), 2)
                else:
                    self._draw_fallback(screen)
            except:
                self._draw_fallback(screen)

    def _draw_fallback(self, screen):
        """Fallback bomb drawing"""
        # Draw bomb body
        pygame.draw.circle(screen, (0, 0, 0),
                           (self.rect.centerx, self.rect.centery),
                           TILE_SIZE // 3)

        # Draw fuse
        fuse_length = int((self.timer / BOMB_TIMER) * 10)
        if fuse_length > 0:
            pygame.draw.line(screen, (255, 100, 0),
                             (self.rect.centerx, self.rect.centery - TILE_SIZE // 3),
                             (self.rect.centerx, self.rect.centery - TILE_SIZE // 3 - fuse_length),
                             2)


class Explosion:
    """
    Explosion effect that appears after bomb detonation.
    Now with animated frames!
    """

    def __init__(self, x, y, direction=None):
        """
        Initialize explosion.

        Args:
            x (int): Grid X position
            y (int): Grid Y position
            direction (str): Direction of explosion ('up', 'down', 'left', 'right', or None for center)
        """
        self.grid_x = x
        self.grid_y = y
        self.direction = direction

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

        # Animation
        self.duration = 500  # milliseconds
        self.frame = 0
        self.frame_time = 0
        self.frame_duration = 500 / 8  # 8 frames

    def update(self, dt):
        """
        Update explosion animation.

        Args:
            dt (int): Delta time in milliseconds

        Returns:
            bool: True if explosion is finished
        """
        self.duration -= dt
        self.frame_time += dt

        if self.frame_time >= self.frame_duration:
            self.frame += 1
            self.frame_time = 0

        return self.duration <= 0

    def draw(self, screen):
        """Draw explosion effect with animation frames"""
        if self.duration > 0:
            try:
                from assets.asset_loader import get_asset_loader
                loader = get_asset_loader()
                frames = loader.get_image('explosion_frames')

                if frames and self.frame < len(frames):
                    frame_surface = frames[self.frame]
                    screen.blit(frame_surface, (self.x, self.y))
                else:
                    self._draw_fallback(screen)
            except:
                self._draw_fallback(screen)

    def _draw_fallback(self, screen):
        """Fallback explosion drawing"""
        # Create surface with alpha
        explosion_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        alpha = int((self.duration / 500) * 255)
        explosion_surface.set_alpha(alpha)

        # Draw explosion based on direction
        if self.direction is None:
            # Center explosion (circle)
            pygame.draw.circle(explosion_surface, (255, 150, 0),
                               (TILE_SIZE // 2, TILE_SIZE // 2),
                               TILE_SIZE // 2)
        else:
            # Directional explosion (beam)
            if self.direction in ['left', 'right']:
                pygame.draw.rect(explosion_surface, (255, 150, 0),
                                 (0, TILE_SIZE // 4, TILE_SIZE, TILE_SIZE // 2))
            else:  # up or down
                pygame.draw.rect(explosion_surface, (255, 150, 0),
                                 (TILE_SIZE // 4, 0, TILE_SIZE // 2, TILE_SIZE))

        screen.blit(explosion_surface, (self.x, self.y))