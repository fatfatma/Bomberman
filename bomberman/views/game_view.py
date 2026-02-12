# views/game_view.py
"""
MVC Pattern - Game View
Handles all rendering and visual presentation
"""

import pygame
from config import *


class GameView:
    """
    View component of MVC pattern.
    Responsible for rendering the game state.
    """

    def __init__(self, screen):
        """
        Initialize game view.

        Args:
            screen: Pygame screen surface
        """
        self.screen = screen
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 48)

    def render(self, game_state):
        """
        Render the entire game state.

        Args:
            game_state (dict): Current game state from controller
        """
        # Clear screen
        self.screen.fill((50, 50, 50))

        # Draw grid
        self._draw_grid()

        # Draw game objects
        self._draw_walls(game_state['walls'])
        self._draw_explosions(game_state['explosions'])
        self._draw_powerups(game_state['powerups'])
        self._draw_bombs(game_state['bombs'])
        self._draw_enemies(game_state['enemies'])
        self._draw_players(game_state['players'])

        # Draw UI
        self._draw_ui(game_state)

        # Draw game over if needed
        if game_state['game_over']:
            self._draw_game_over(
                game_state['winner'],
                game_state.get('is_single_player', False),
                game_state.get('winner_label')
            )

        # Update display
        pygame.display.flip()

    def _draw_grid(self):
        """Draw background grid"""
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, (70, 70, 70), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(self.screen, (70, 70, 70), (0, y), (SCREEN_WIDTH, y))

    def _draw_walls(self, walls):
        """Draw walls"""
        for wall in walls:
            if not wall.destroyed:
                wall.draw(self.screen)

    def _draw_explosions(self, explosions):
        """Draw explosions"""
        for explosion in explosions:
            explosion.draw(self.screen)

    def _draw_powerups(self, powerups):
        """Draw power-ups"""
        for powerup in powerups:
            powerup.draw(self.screen)

    def _draw_bombs(self, bombs):
        """Draw bombs"""
        for bomb in bombs:
            bomb.draw(self.screen)

    def _draw_enemies(self, enemies):
        """Draw enemies"""
        for enemy in enemies:
            enemy.draw(self.screen)

    def _draw_players(self, players):
        """Draw players"""
        for player in players:
            player.draw(self.screen)

    def _draw_ui(self, game_state):
        """Draw user interface"""
        players = game_state['players']
        score = game_state['score']
        stats = game_state['stats']

        # Player 1 info (top left)
        if len(players) > 0:
            p1 = players[0]
            status = "ALIVE" if p1.state_manager.is_alive() else "DEAD"
            color = GREEN if p1.state_manager.is_alive() else RED

            texts = [
                (f"{p1.name} (P1)", WHITE),
                (f"Status: {status}", color),
                (f"Bombs: {p1.bombs_placed}/{p1.bomb_count}", WHITE),
                (f"Power: {p1.bomb_power}", WHITE),
                (f"Speed: {p1.speed}", WHITE),
            ]

            y_offset = 10
            for text, text_color in texts:
                surface = self.font_small.render(text, True, text_color)
                self.screen.blit(surface, (10, y_offset))
                y_offset += 22

        # Player 2 info (top right)
        if len(players) > 1:
            p2 = players[1]
            status = "ALIVE" if p2.state_manager.is_alive() else "DEAD"
            color = GREEN if p2.state_manager.is_alive() else RED

            texts = [
                (f"{p2.name} (P2)", WHITE),
                (f"Status: {status}", color),
                (f"Bombs: {p2.bombs_placed}/{p2.bomb_count}", WHITE),
                (f"Power: {p2.bomb_power}", WHITE),
                (f"Speed: {p2.speed}", WHITE),
            ]

            y_offset = 10
            for text, text_color in texts:
                surface = self.font_small.render(text, True, text_color)
                text_rect = surface.get_rect()
                self.screen.blit(surface, (SCREEN_WIDTH - text_rect.width - 10, y_offset))
                y_offset += 22

        # Score and stats (bottom center)
        score_text = self.font_medium.render(f"Score: {score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(score_text, score_rect)

        stats_text = f"Bombs: {stats['bombs_placed']} | Walls: {stats['walls_destroyed']} | Enemies: {stats['enemies_killed']}"
        stats_surface = self.font_small.render(stats_text, True, WHITE)
        stats_rect = stats_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(stats_surface, stats_rect)

        # Controls hint (bottom left)
        controls = [
            "P1: WASD + SPACE",
            "P2: Arrows + ENTER",
            "ESC: Pause"
        ]

        y_offset = SCREEN_HEIGHT - 80
        for control in controls:
            surface = self.font_small.render(control, True, (150, 150, 150))
            self.screen.blit(surface, (10, y_offset))
            y_offset += 20

    def _draw_game_over(self, winner, is_single_player=False, winner_label=None):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Game over text
        if winner:
            text = f"{winner.name} WINS!"
            color = winner.color
        elif winner_label:
            text = f"{winner_label} WINS!"
            color = BLUE if is_single_player else YELLOW
        else:
            text = "YOU DIED" if is_single_player else "DRAW!"
            color = RED if is_single_player else YELLOW

        game_over_text = self.font_large.render(text, True, color)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)

        # Restart hint
        hint_text = self.font_medium.render("Press R to restart or ESC to quit", True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(hint_text, hint_rect)

    def render_menu(self, title, options, selected_index):
        """
        Render a menu screen.

        Args:
            title (str): Menu title
            options (list): List of menu options
            selected_index (int): Currently selected option index
        """
        self.screen.fill((30, 30, 30))

        # Title
        title_surface = self.font_large.render(title, True, YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_surface, title_rect)

        # Options
        y_offset = 250
        for i, option in enumerate(options):
            color = GREEN if i == selected_index else WHITE
            option_surface = self.font_medium.render(option, True, color)
            option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(option_surface, option_rect)
            y_offset += 60

        pygame.display.flip()

    def render_loading(self, message):
        """Render loading screen"""
        self.screen.fill((30, 30, 30))

        loading_text = self.font_large.render(message, True, WHITE)
        loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(loading_text, loading_rect)

        pygame.display.flip()