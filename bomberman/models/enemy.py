# models/enemy.py
"""
Enemy model for the Bomberman game
Uses Strategy Pattern for different AI behaviors
"""

import pygame
from config import TILE_SIZE, ENEMY_SPEED


class Enemy:
    """
    Enemy class that can have different AI strategies.
    """

    def __init__(self, enemy_id, x, y, color, ai_strategy):
        """
        Initialize enemy.

        Args:
            enemy_id (int): Unique enemy identifier
            x (int): Starting X grid position
            y (int): Starting Y grid position
            color (tuple): RGB color
            ai_strategy (AIStrategy): AI behavior strategy
        """
        self.enemy_id = enemy_id
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.color = color
        self.speed = ENEMY_SPEED
        self.alive = True

        # AI Strategy
        self.ai_strategy = ai_strategy

        # Rectangle for collision
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE - 4, TILE_SIZE - 4)

        # Animation
        self.animation_timer = 0
        self.animation_frame = 0

    def set_strategy(self, ai_strategy):
        """
        Change AI strategy at runtime (Strategy Pattern).

        Args:
            ai_strategy (AIStrategy): New AI strategy
        """
        self.ai_strategy = ai_strategy
        print(f"Enemy {self.enemy_id} strategy changed to {ai_strategy.__class__.__name__}")

    def update(self, dt, walls, players, enemies):
        """
        Update enemy position using AI strategy.

        Args:
            dt (int): Delta time in milliseconds
            walls (list): List of walls
            players (list): List of players
            enemies (list): List of other enemies
        """
        if not self.alive:
            return

        # Get movement direction from AI strategy
        dx, dy = self.ai_strategy.calculate_move(self, walls, players, enemies)

        # Move enemy
        self.move(dx, dy, walls, enemies)

        # Update animation
        self.animation_timer += dt
        if self.animation_timer > 200:
            self.animation_frame = (self.animation_frame + 1) % 2
            self.animation_timer = 0

    def move(self, dx, dy, walls, enemies):
        """
        Move enemy with collision detection.

        Args:
            dx (int): X direction (-1, 0, or 1)
            dy (int): Y direction (-1, 0, or 1)
            walls (list): List of walls
            enemies (list): List of other enemies
        """
        if not self.alive:
            return

        # Calculate new position
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        new_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)

        # Check collision with walls
        collision = False
        for wall in walls:
            if not wall.destroyed and new_rect.colliderect(wall.rect):
                collision = True
                break

        # Check collision with other enemies
        for enemy in enemies:
            if enemy != self and enemy.alive and new_rect.colliderect(enemy.rect):
                collision = True
                break

        # Update position if no collision
        if not collision:
            self.x = new_x
            self.y = new_y
            self.rect.x = new_x
            self.rect.y = new_y
            self.update_grid_position()

    def update_grid_position(self):
        """Update grid position based on pixel position"""
        self.grid_x = self.x // TILE_SIZE
        self.grid_y = self.y // TILE_SIZE

    def die(self):
        """Kill the enemy"""
        self.alive = False

    def draw(self, screen):
        """Draw enemy on screen"""
        if self.alive:
            # Draw enemy body (skull shape)
            pygame.draw.circle(screen, self.color,
                               (self.rect.centerx, self.rect.centery),
                               TILE_SIZE // 3)

            # Draw eyes (evil look)
            eye_size = 3
            if self.animation_frame == 0:
                # Normal eyes
                pygame.draw.circle(screen, (255, 0, 0),
                                   (self.rect.centerx - 5, self.rect.centery - 2), eye_size)
                pygame.draw.circle(screen, (255, 0, 0),
                                   (self.rect.centerx + 5, self.rect.centery - 2), eye_size)
            else:
                # Blinking
                pygame.draw.line(screen, (255, 0, 0),
                                 (self.rect.centerx - 7, self.rect.centery - 2),
                                 (self.rect.centerx - 3, self.rect.centery - 2), 2)
                pygame.draw.line(screen, (255, 0, 0),
                                 (self.rect.centerx + 3, self.rect.centery - 2),
                                 (self.rect.centerx + 7, self.rect.centery - 2), 2)

            # Draw mouth (evil grin)
            pygame.draw.arc(screen, (255, 0, 0),
                            pygame.Rect(self.rect.centerx - 8, self.rect.centery + 2, 16, 8),
                            3.14, 0, 2)

            # Draw AI type indicator
            font = pygame.font.Font(None, 16)
            ai_type = self.ai_strategy.__class__.__name__.replace('AIStrategy', '')
            text = font.render(ai_type[0], True, (255, 255, 255))
            screen.blit(text, (self.rect.x + 2, self.rect.y + 2))