# views/menu_view.py
"""
Menu View - Main menu and login screens
"""

import pygame
from config import *


class MenuView:
    """
    View for menu screens.
    """

    def __init__(self, screen):
        """Initialize menu view"""
        self.screen = screen
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 64)
        self.font_title = pygame.font.Font(None, 80)

    def render_main_menu(self, options, selected_index):
        """
        Render main menu.

        Args:
            options (list): List of menu options
            selected_index (int): Currently selected option
        """
        self.screen.fill((20, 20, 30))

        # Animated title
        import math
        import time
        offset = int(math.sin(time.time() * 2) * 10)

        # Title with shadow
        title = "BOMBERMAN"
        shadow = self.font_title.render(title, True, (50, 50, 50))
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 5, 120 + offset + 5))
        self.screen.blit(shadow, shadow_rect)

        title_surface = self.font_title.render(title, True, YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120 + offset))
        self.screen.blit(title_surface, title_rect)

        # Subtitle
        subtitle = "Design Patterns Project"
        subtitle_surface = self.font_small.render(subtitle, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(subtitle_surface, subtitle_rect)

        # Menu options
        y_offset = 280
        for i, option in enumerate(options):
            # Highlight selected option
            if i == selected_index:
                color = GREEN
                # Draw selection box
                box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y_offset - 10, 400, 50)
                pygame.draw.rect(self.screen, (0, 100, 0), box_rect, 3, border_radius=10)
            else:
                color = WHITE

            option_surface = self.font_medium.render(option, True, color)
            option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 10))
            self.screen.blit(option_surface, option_rect)
            y_offset += 70

        # Instructions
        instructions = [
            "Use ↑/↓ to navigate",
            "Press ENTER to select"
        ]

        y_offset = SCREEN_HEIGHT - 80
        for instruction in instructions:
            inst_surface = self.font_small.render(instruction, True, (150, 150, 150))
            inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(inst_surface, inst_rect)
            y_offset += 30

        pygame.display.flip()

    def render_login(self, username_input, in_username_field):
        """
        Render login screen.

        Args:
            username_input (str): Current username input
            in_username_field (bool): Whether username field is active
        """
        self.screen.fill((20, 20, 30))

        # Title
        title = "Enter Your Name"
        title_surface = self.font_large.render(title, True, YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surface, title_rect)

        # Username field
        field_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 250, 400, 60)
        field_color = GREEN if in_username_field else (100, 100, 100)
        pygame.draw.rect(self.screen, field_color, field_rect, 3, border_radius=10)

        # Username text
        username_text = username_input if username_input else "Username..."
        text_color = WHITE if username_input else (100, 100, 100)
        username_surface = self.font_medium.render(username_text, True, text_color)
        username_rect = username_surface.get_rect(center=field_rect.center)
        self.screen.blit(username_surface, username_rect)

        # Cursor
        if in_username_field:
            cursor_x = username_rect.right + 5
            cursor_y = username_rect.centery
            pygame.draw.line(self.screen, WHITE,
                             (cursor_x, cursor_y - 15),
                             (cursor_x, cursor_y + 15), 2)

        # Instructions
        instructions = [
            "Type your username",
            "Press ENTER to continue",
            "Press ESC to go back"
        ]

        y_offset = 400
        for instruction in instructions:
            inst_surface = self.font_small.render(instruction, True, (150, 150, 150))
            inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(inst_surface, inst_rect)
            y_offset += 35

        pygame.display.flip()

    def render_waiting(self, message):
        """
        Render waiting screen.

        Args:
            message (str): Waiting message
        """
        self.screen.fill((20, 20, 30))

        # Animated dots
        import time
        dots = "." * (int(time.time() * 2) % 4)

        # Message
        text = f"{message}{dots}"
        text_surface = self.font_large.render(text, True, YELLOW)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text_surface, text_rect)

        # Spinner animation
        import math
        angle = time.time() * 5
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        radius = 30

        for i in range(8):
            a = angle + (i * math.pi / 4)
            x = center[0] + int(math.cos(a) * radius)
            y = center[1] + int(math.sin(a) * radius)
            alpha = int(255 * (i / 8))
            color = (alpha, alpha, 0)
            pygame.draw.circle(self.screen, color, (x, y), 5)

        # Cancel instruction
        inst = "Press ESC to cancel"
        inst_surface = self.font_small.render(inst, True, (150, 150, 150))
        inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(inst_surface, inst_rect)

        pygame.display.flip()

    def render_menu(self, title, options, selected_index):
        """
        Render generic menu screen.

        Args:
            title (str): Menu title
            options (list): List of menu options
            selected_index (int): Currently selected option
        """
        self.screen.fill((20, 20, 30))

        # Title
        title_surface = self.font_large.render(title, True, YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(title_surface, title_rect)

        # Menu options
        y_offset = 250
        for i, option in enumerate(options):
            # Highlight selected option
            if i == selected_index:
                color = GREEN
                # Draw selection box
                box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y_offset - 10, 400, 50)
                pygame.draw.rect(self.screen, (0, 100, 0), box_rect, 3, border_radius=10)
            else:
                color = WHITE

            option_surface = self.font_medium.render(option, True, color)
            option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 10))
            self.screen.blit(option_surface, option_rect)
            y_offset += 70

        # Instructions
        instructions = [
            "Use ↑/↓ to navigate",
            "Press ENTER to select",
            "Press ESC to go back"
        ]

        y_offset = SCREEN_HEIGHT - 120
        for instruction in instructions:
            inst_surface = self.font_small.render(instruction, True, (150, 150, 150))
            inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(inst_surface, inst_rect)
            y_offset += 30

        pygame.display.flip()

    def render_connection_error(self):
        """Render connection error screen"""
        self.screen.fill((20, 20, 30))

        # Error message
        error = "Connection Failed!"
        error_surface = self.font_large.render(error, True, RED)
        error_rect = error_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(error_surface, error_rect)

        # Details
        details = [
            "Could not connect to server",
            "Make sure the server is running",
            "",
            "Press any key to return to menu"
        ]

        y_offset = SCREEN_HEIGHT // 2 + 30
        for detail in details:
            detail_surface = self.font_small.render(detail, True, WHITE)
            detail_rect = detail_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(detail_surface, detail_rect)
            y_offset += 35

        pygame.display.flip()