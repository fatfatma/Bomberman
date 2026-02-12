# views/leaderboard_view.py
"""
Leaderboard View - Display high scores
"""

import pygame
from config import *


class LeaderboardView:
    """
    View for displaying leaderboard.
    """

    def __init__(self, screen):
        """Initialize leaderboard view"""
        self.screen = screen
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 48)

    def render(self, leaderboard_entries):
        """
        Render leaderboard screen.

        Args:
            leaderboard_entries (list): List of LeaderboardEntry objects
        """
        self.screen.fill((20, 20, 30))

        # Title
        title = "🏆 LEADERBOARD 🏆"
        title_surface = self.font_large.render(title, True, YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_surface, title_rect)

        # Header
        header_y = 150
        header_texts = [
            ("Rank", 100),
            ("Player", 250),
            ("Score", 450),
            ("Date", 600)
        ]

        for text, x in header_texts:
            header_surface = self.font_medium.render(text, True, WHITE)
            self.screen.blit(header_surface, (x, header_y))

        # Draw separator line
        pygame.draw.line(self.screen, WHITE,
                         (80, header_y + 40),
                         (SCREEN_WIDTH - 80, header_y + 40), 2)

        # Leaderboard entries
        y_offset = header_y + 60

        if not leaderboard_entries:
            # No entries message
            no_entries = "No scores yet. Be the first!"
            no_entries_surface = self.font_medium.render(no_entries, True, (150, 150, 150))
            no_entries_rect = no_entries_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 50))
            self.screen.blit(no_entries_surface, no_entries_rect)
        else:
            # Display entries
            for i, entry in enumerate(leaderboard_entries[:10], 1):
                # Medal colors for top 3
                if i == 1:
                    rank_color = (255, 215, 0)  # Gold
                    medal = "🥇"
                elif i == 2:
                    rank_color = (192, 192, 192)  # Silver
                    medal = "🥈"
                elif i == 3:
                    rank_color = (205, 127, 50)  # Bronze
                    medal = "🥉"
                else:
                    rank_color = WHITE
                    medal = ""

                # Rank
                rank_text = f"{medal} #{i}"
                rank_surface = self.font_medium.render(rank_text, True, rank_color)
                self.screen.blit(rank_surface, (100, y_offset))

                # Player name
                name_surface = self.font_medium.render(entry.username, True, WHITE)
                self.screen.blit(name_surface, (250, y_offset))

                # Score
                score_surface = self.font_medium.render(str(entry.score), True, GREEN)
                self.screen.blit(score_surface, (450, y_offset))

                # Date (formatted)
                date_str = entry.game_date.strftime("%d/%m/%Y") if entry.game_date else "N/A"
                date_surface = self.font_small.render(date_str, True, (150, 150, 150))
                self.screen.blit(date_surface, (600, y_offset + 5))

                y_offset += 45

        # Instructions
        instructions = "Press ESC to return to menu"
        inst_surface = self.font_small.render(instructions, True, (150, 150, 150))
        inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(inst_surface, inst_rect)

        pygame.display.flip()

    def render_user_stats(self, username, stats, best_score):
        """
        Render user statistics screen.

        Args:
            username (str): Username
            stats (GameStats): User's game statistics
            best_score (int): User's best score
        """
        self.screen.fill((20, 20, 30))

        # Title
        title = f"📊 {username}'s Statistics"
        title_surface = self.font_large.render(title, True, YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_surface, title_rect)

        # Stats boxes
        stats_data = [
            ("Total Games", stats.total_games, GREEN),
            ("Wins", stats.wins, BLUE),
            ("Losses", stats.losses, RED),
            ("Best Score", best_score, YELLOW)
        ]

        # Win rate
        if stats.total_games > 0:
            win_rate = (stats.wins / stats.total_games) * 100
            stats_data.append(("Win Rate", f"{win_rate:.1f}%", (0, 255, 255)))

        # Draw stats in grid
        box_width = 200
        box_height = 100
        spacing = 30
        start_x = (SCREEN_WIDTH - (box_width * 2 + spacing)) // 2
        start_y = 200

        for i, (label, value, color) in enumerate(stats_data):
            row = i // 2
            col = i % 2

            x = start_x + col * (box_width + spacing)
            y = start_y + row * (box_height + spacing)

            # Draw box
            box_rect = pygame.Rect(x, y, box_width, box_height)
            pygame.draw.rect(self.screen, color, box_rect, 3, border_radius=10)

            # Draw label
            label_surface = self.font_small.render(label, True, WHITE)
            label_rect = label_surface.get_rect(center=(x + box_width // 2, y + 25))
            self.screen.blit(label_surface, label_rect)

            # Draw value
            value_surface = self.font_large.render(str(value), True, color)
            value_rect = value_surface.get_rect(center=(x + box_width // 2, y + 60))
            self.screen.blit(value_surface, value_rect)

        # Instructions
        instructions = "Press ESC to return"
        inst_surface = self.font_small.render(instructions, True, (150, 150, 150))
        inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(inst_surface, inst_rect)

        pygame.display.flip()