# patterns/behavioral/state.py
"""
State Pattern - Player State Management
Manages different states of the player (Normal, Invincible, Stunned, Dead)
"""

from abc import ABC, abstractmethod
import pygame


class PlayerState(ABC):
    """
    Abstract state class for player states.
    """

    def __init__(self, player):
        self.player = player

    @abstractmethod
    def handle_input(self, keys):
        """
        Handle player input based on current state.

        Args:
            keys: Pygame key states
        """
        pass

    @abstractmethod
    def update(self, dt):
        """
        Update state logic.

        Args:
            dt (int): Delta time in milliseconds
        """
        pass

    @abstractmethod
    def take_damage(self):
        """
        Handle damage to player.

        Returns:
            bool: True if player died
        """
        pass

    @abstractmethod
    def draw(self, screen):
        """
        Draw player based on current state.

        Args:
            screen: Pygame screen surface
        """
        pass

    @abstractmethod
    def get_state_name(self):
        """Return the name of the state"""
        pass


class NormalState(PlayerState):
    """
    Normal state - Player can move and take damage normally.
    """

    def handle_input(self, keys):
        """Handle normal movement"""
        dx = dy = 0
        if keys[self.player.controls['left']]:
            dx = -1
        if keys[self.player.controls['right']]:
            dx = 1
        if keys[self.player.controls['up']]:
            dy = -1
        if keys[self.player.controls['down']]:
            dy = 1
        return dx, dy

    def update(self, dt):
        """Normal update - no special effects"""
        pass

    def take_damage(self):
        """Normal damage - player dies"""
        self.player.state_manager.change_state(DeadState(self.player))
        return True

    def draw(self, screen):
        """Draw normal player - handled by Player.draw()"""
        pass

    def get_state_name(self):
        return "Normal"


class InvincibleState(PlayerState):
    """
    Invincible state - Player cannot take damage for a duration.
    Visual effect: Flashing/glowing appearance.
    """

    def __init__(self, player, duration=3000):
        super().__init__(player)
        self.duration = duration
        self.timer = duration
        self.flash_timer = 0
        self.visible = True

    def handle_input(self, keys):
        """Handle movement (same as normal)"""
        dx = dy = 0
        if keys[self.player.controls['left']]:
            dx = -1
        if keys[self.player.controls['right']]:
            dx = 1
        if keys[self.player.controls['up']]:
            dy = -1
        if keys[self.player.controls['down']]:
            dy = 1
        return dx, dy

    def update(self, dt):
        """Update invincibility timer"""
        self.timer -= dt
        self.flash_timer += dt

        # Flashing effect
        if self.flash_timer > 100:
            self.visible = not self.visible
            self.flash_timer = 0

        # Return to normal state when timer expires
        if self.timer <= 0:
            self.player.state_manager.change_state(NormalState(self.player))
            print(f"Player {self.player.player_id} invincibility ended")

    def take_damage(self):
        """No damage while invincible"""
        print(f"Player {self.player.player_id} is invincible!")
        return False

    def draw(self, screen):
        """Draw with flashing effect - handled by Player.draw()"""
        pass

    def get_state_name(self):
        return f"Invincible ({self.timer // 1000}s)"


class StunnedState(PlayerState):
    """
    Stunned state - Player cannot move for a duration.
    Visual effect: Stars around player, darker color.
    """

    def __init__(self, player, duration=2000):
        super().__init__(player)
        self.duration = duration
        self.timer = duration
        self.star_timer = 0
        self.star_rotation = 0

    def handle_input(self, keys):
        """Cannot move while stunned"""
        return 0, 0

    def update(self, dt):
        """Update stun timer"""
        self.timer -= dt
        self.star_timer += dt
        self.star_rotation += dt * 0.5

        # Return to normal state when timer expires
        if self.timer <= 0:
            self.player.state_manager.change_state(NormalState(self.player))
            print(f"Player {self.player.player_id} is no longer stunned")

    def take_damage(self):
        """Can take damage while stunned"""
        self.player.state_manager.change_state(DeadState(self.player))
        return True

    def draw(self, screen):
        """Draw with stun effect - handled by Player.draw()"""
        pass

    def get_state_name(self):
        return f"Stunned ({self.timer // 1000}s)"


class DeadState(PlayerState):
    """
    Dead state - Player is dead and cannot do anything.
    Visual effect: Explosion animation, then disappear.
    """

    def __init__(self, player):
        super().__init__(player)
        self.animation_timer = 1000  # 1 second death animation
        self.explosion_radius = 5

    def handle_input(self, keys):
        """Cannot move while dead"""
        return 0, 0

    def update(self, dt):
        """Update death animation"""
        self.animation_timer -= dt
        self.explosion_radius += dt * 0.05

    def take_damage(self):
        """Already dead"""
        return False

    def draw(self, screen):
        """Draw death animation - handled by Player.draw()"""
        pass

    def get_state_name(self):
        return "Dead"


class PlayerStateManager:
    """
    Manages player state transitions.
    This is added to the Player class.
    """

    def __init__(self, player):
        self.player = player
        self.current_state = NormalState(player)

    def change_state(self, new_state):
        """Change to a new state"""
        old_state_name = self.current_state.get_state_name()
        self.current_state = new_state
        new_state_name = self.current_state.get_state_name()
        print(f"Player {self.player.player_id} state: {old_state_name} → {new_state_name}")

    def handle_input(self, keys):
        """Delegate input handling to current state"""
        return self.current_state.handle_input(keys)

    def update(self, dt):
        """Delegate update to current state"""
        self.current_state.update(dt)

    def take_damage(self):
        """Delegate damage handling to current state"""
        return self.current_state.take_damage()

    def draw(self, screen):
        """Delegate drawing to current state"""
        self.current_state.draw(screen)

    def get_state_name(self):
        """Get current state name"""
        return self.current_state.get_state_name()
    
    def is_alive(self):
        """Check if player is alive (not in DeadState)"""
        return not isinstance(self.current_state, DeadState)
    
    def set_normal_state(self):
        """Set player to normal state"""
        self.change_state(NormalState(self.player))
    
    def set_invincible_state(self, duration=5000):
        """Set player to invincible state"""
        self.change_state(InvincibleState(self.player, duration))
    
    def set_stunned_state(self, duration=2000):
        """Set player to stunned state"""
        self.change_state(StunnedState(self.player, duration))
    
    def set_dead_state(self):
        """Set player to dead state"""
        self.change_state(DeadState(self.player))
    
    def draw_state_indicator(self, screen, rect):
        """Draw visual indicator of current state"""
        import pygame
        if isinstance(self.current_state, InvincibleState):
            # Draw golden glow for invincible state
            pygame.draw.circle(screen, (255, 215, 0), rect.center, rect.width // 2 + 3, 2)
        elif isinstance(self.current_state, StunnedState):
            # Draw red border for stunned state
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)


# Usage Example
if __name__ == "__main__":
    print("=== Testing State Pattern ===\n")

    print("Player States:")
    print("  1. Normal - Can move and take damage")
    print("  2. Invincible - Cannot take damage (flashing effect)")
    print("  3. Stunned - Cannot move (stars around player)")
    print("  4. Dead - Game over for player")

    print("\nState transitions:")
    print("  Normal → Invincible (collect special power-up)")
    print("  Normal → Stunned (hit by special bomb)")
    print("  Normal/Stunned → Dead (take damage)")
    print("  Invincible → Normal (timer expires)")
    print("  Stunned → Normal (timer expires)")

    print("\n✅ State Pattern test completed!")