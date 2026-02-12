# models/player.py
"""
Player model for the Bomberman game
Implements State Pattern for player state management
"""

import pygame
from config import TILE_SIZE, PLAYER_SPEED, INITIAL_BOMB_COUNT, INITIAL_BOMB_POWER
from patterns.behavioral.state import PlayerStateManager


class Player:
    """
    Player class representing a player in the game.
    Handles movement, bomb placement, and power-ups.
    """

    def __init__(self, player_id, x, y, color, controls):
        """
        Initialize player.

        Args:
            player_id (int): Unique player identifier (1 or 2)
            x (int): Starting X grid position
            y (int): Starting Y grid position
            color (tuple): RGB color for player
            controls (dict): Keyboard controls for this player
        """
        self.player_id = player_id
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.grid_x = x
        self.grid_y = y
        self.color = color
        self.controls = controls

        # Player stats
        self.speed = PLAYER_SPEED
        self.bomb_count = INITIAL_BOMB_COUNT
        self.bomb_power = INITIAL_BOMB_POWER
        self.bombs_placed = 0

        # Rectangle for collision detection
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE - 4, TILE_SIZE - 4)

        # Animation
        self.direction = 'down'  # Current facing direction
        
        # State Pattern Implementation
        self.state_manager = PlayerStateManager(self)
        self.state_manager.set_normal_state()

    def update_grid_position(self):
        """Update grid position based on pixel position"""
        self.grid_x = self.x // TILE_SIZE
        self.grid_y = self.y // TILE_SIZE

    def move(self, dx, dy, walls):
        """
        Move player with classic Bomberman mechanics:
        - Axis locking for smooth transitions
        - Corner sliding for easier navigation

        Args:
            dx (int): X direction (-1, 0, or 1)
            dy (int): Y direction (-1, 0, or 1)
            walls (list): List of wall objects to check collision
        """
        # Check if stunned - if so, don't allow movement
        if hasattr(self.state_manager.current_state, '__class__'):
            state_name = self.state_manager.current_state.get_state_name()
            if 'Stunned' in state_name:
                dx = dy = 0
        
        if not self.state_manager.is_alive():
            return

        # Update direction
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'

        # Simple axis locking: align to grid on perpendicular axis BEFORE moving
        align_threshold = 8
        
        if dx != 0:  # Moving horizontally, align Y
            grid_center_y = self.grid_y * TILE_SIZE
            if abs(self.y - grid_center_y) < align_threshold:
                self.y = grid_center_y
                self.rect.y = self.y
        
        if dy != 0:  # Moving vertically, align X
            grid_center_x = self.grid_x * TILE_SIZE
            if abs(self.x - grid_center_x) < align_threshold:
                self.x = grid_center_x
                self.rect.x = self.x

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

        # Update position if no collision
        if not collision:
            self.x = new_x
            self.y = new_y
            self.rect.x = new_x
            self.rect.y = new_y
            self.update_grid_position()

    def can_place_bomb(self):
        """Check if player can place a bomb"""
        return self.state_manager.is_alive() and self.bombs_placed < self.bomb_count

    def place_bomb(self):
        """Place a bomb (increment counter)"""
        if self.can_place_bomb():
            self.bombs_placed += 1
            return True
        return False

    def bomb_exploded(self):
        """Called when one of player's bombs explodes"""
        if self.bombs_placed > 0:
            self.bombs_placed -= 1

    def add_bomb_count(self):
        """Power-up: Increase bomb count"""
        self.bomb_count += 1

    def add_bomb_power(self):
        """Power-up: Increase bomb explosion range"""
        self.bomb_power += 1

    def add_speed(self):
        """Power-up: Increase movement speed"""
        self.speed += 1
    
    def apply_invincibility(self, duration=5000):
        """Apply invincibility state (power-up)
        
        Args:
            duration (int): Duration in milliseconds
        """
        self.state_manager.set_invincible_state(duration)
    
    def stun(self, duration=2000):
        """Stun the player (temporary immobilization)
        
        Args:
            duration (int): Duration in milliseconds
        """
        self.state_manager.set_stunned_state(duration)

    def die(self):
        """Kill the player"""
        self.state_manager.set_dead_state()

    def draw(self, screen):
        """Draw the player on screen"""
        if self.state_manager.is_alive():
            # Draw player body
            pygame.draw.circle(screen, self.color,
                               (self.rect.centerx, self.rect.centery),
                               TILE_SIZE // 3)

            # Draw player eyes based on direction
            eye_offset = 5
            if self.direction == 'right':
                eye1 = (self.rect.centerx + eye_offset, self.rect.centery - 3)
                eye2 = (self.rect.centerx + eye_offset, self.rect.centery + 3)
            elif self.direction == 'left':
                eye1 = (self.rect.centerx - eye_offset, self.rect.centery - 3)
                eye2 = (self.rect.centerx - eye_offset, self.rect.centery + 3)
            elif self.direction == 'up':
                eye1 = (self.rect.centerx - 3, self.rect.centery - eye_offset)
                eye2 = (self.rect.centerx + 3, self.rect.centery - eye_offset)
            else:  # down
                eye1 = (self.rect.centerx - 3, self.rect.centery + eye_offset)
                eye2 = (self.rect.centerx + 3, self.rect.centery + eye_offset)

            pygame.draw.circle(screen, (0, 0, 0), eye1, 2)
            pygame.draw.circle(screen, (0, 0, 0), eye2, 2)
            
            # Draw state indicator (invincible = glow, stunned = red border)
            self.state_manager.draw_state_indicator(screen, self.rect)

            # Draw player ID
            font = pygame.font.Font(None, 20)
            text = font.render(f"P{self.player_id}", True, (255, 255, 255))
            screen.blit(text, (self.rect.x + 5, self.rect.y + 5))