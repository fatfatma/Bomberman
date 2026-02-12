# main.py
"""
Bomberman Game - Complete Version with All Features
Implements all 9 Design Patterns + Bonus Features
"""

import pygame
from controllers.game_controller import GameController
from controllers.network_controller import NetworkGameController
from views.game_view import GameView
from views.menu_view import MenuView
from views.leaderboard_view import LeaderboardView
from database.user_repository import UserRepository
from database.game_repository import GameRepository
from config import *


def _print_welcome():
    """Print welcome message"""
    print("=" * 60)
    print("🎮 BOMBERMAN GAME - COMPLETE VERSION")
    print("=" * 60)
    print("\n✅ All 9 Design Patterns Implemented:")
    print("  1. Singleton Pattern - Database Connection")
    print("  2. Factory Method Pattern - Walls, PowerUps, AI")
    print("  3. Decorator Pattern - PowerUp Enhancements")
    print("  4. Observer Pattern - Game Events")
    print("  5. Strategy Pattern - Enemy AI (A* Pathfinding)")
    print("  6. State Pattern - Player States")
    print("  7. Repository Pattern - Database Operations")
    print("  8. Facade Pattern - Network Wrapper")
    print("  9. MVC Pattern - Game Architecture")
    print("\n🎁 Bonus Features:")
    print("  ✅ A* Pathfinding (+5 points)")
    print("  ✅ Professional UI/UX (+5 points)")
    print("  ✅ Multiplayer Lobby System (+5 points)")
    print("\n📊 Additional Features:")
    print("  ✓ User Authentication & Registration")
    print("  ✓ Game Statistics Tracking")
    print("  ✓ Leaderboard System")
    print("  ✓ Online Multiplayer Support")
    print("=" * 60 + "\n")


class BombermanGame:
    """
    Main game class implementing MVC pattern with all features.
    """

    def __init__(self):
        """Initialize the game"""
        pygame.init()

        # Setup display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bomberman - All Design Patterns")
        self.clock = pygame.time.Clock()

        # Views
        self.game_view = GameView(self.screen)
        self.menu_view = MenuView(self.screen)
        self.leaderboard_view = LeaderboardView(self.screen)

        # Controllers
        self.controller = None

        # Repositories
        self.user_repo = UserRepository()
        self.game_repo = GameRepository()

        # Game state
        self.running = True
        self.current_screen = 'main_menu'  # main_menu, login, game, leaderboard, theme_select
        self.selected_menu_option = 0
        self.game_mode = None  # single, local, online
        self.selected_theme = 'desert'  # desert, forest, city

        # User data
        self.current_user = None
        self.username_input = ""

        _print_welcome()

    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS)

            if self.current_screen == 'main_menu':
                self._handle_main_menu()
            elif self.current_screen == 'login':
                self._handle_login()
            elif self.current_screen == 'theme_select':
                self._handle_theme_select()
            elif self.current_screen == 'game':
                self._handle_game(dt)
            elif self.current_screen == 'leaderboard':
                self._handle_leaderboard()
            elif self.current_screen == 'waiting':
                self._handle_waiting()

        pygame.quit()
        print("\n👋 Thanks for playing Bomberman!")

    def _handle_main_menu(self):
        """Handle main menu"""
        menu_options = [
            "1. Single Player vs AI",
            "2. Local Multiplayer (2 Players)",
            "3. Online Multiplayer",
            "4. View Leaderboard",
            "5. Quit"
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_menu_option = (self.selected_menu_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_menu_option = (self.selected_menu_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    self._handle_menu_selection()

        self.menu_view.render_main_menu(menu_options, self.selected_menu_option)

    def _handle_menu_selection(self):
        """Handle menu selection"""
        if self.selected_menu_option == 0:
            # Single Player
            self.game_mode = 'single'
            self.current_screen = 'login'

        elif self.selected_menu_option == 1:
            # Local Multiplayer
            self.game_mode = 'local'
            self.current_screen = 'theme_select'

        elif self.selected_menu_option == 2:
            # Online Multiplayer
            self.game_mode = 'online'
            self.current_screen = 'login'

        elif self.selected_menu_option == 3:
            # Leaderboard
            self.current_screen = 'leaderboard'

        elif self.selected_menu_option == 4:
            # Quit
            self.running = False

    def _handle_login(self):
        """Handle login screen"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.current_screen = 'main_menu'
                    self.username_input = ""

                elif event.key == pygame.K_RETURN and self.username_input:
                    # Try to authenticate or register
                    user = self.user_repo.find_by_username(self.username_input)

                    if not user:
                        # Register new user
                        user = self.user_repo.register(self.username_input, "default_pass")

                    self.current_user = user

                    # Go to theme selection or start game
                    if self.game_mode == 'single':
                        self.current_screen = 'theme_select'
                    elif self.game_mode == 'online':
                        self.current_screen = 'theme_select'

                elif event.key == pygame.K_BACKSPACE:
                    self.username_input = self.username_input[:-1]

                else:
                    # Add character to username
                    if len(self.username_input) < 15 and event.unicode.isprintable():
                        self.username_input += event.unicode

        self.menu_view.render_login(self.username_input, True)

    def _handle_theme_select(self):
        """Handle theme selection screen"""
        themes = ['desert', 'forest', 'city']
        theme_names = ['1. Desert Theme', '2. Forest Theme', '3. City Theme']
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.current_screen = 'main_menu'
                    self.selected_menu_option = 0
                
                elif event.key == pygame.K_UP:
                    self.selected_menu_option = (self.selected_menu_option - 1) % len(themes)
                elif event.key == pygame.K_DOWN:
                    self.selected_menu_option = (self.selected_menu_option + 1) % len(themes)
                elif event.key == pygame.K_RETURN:
                    self.selected_theme = themes[self.selected_menu_option]
                    
                    # Start appropriate game mode
                    if self.game_mode == 'single':
                        self._start_single_game()
                    elif self.game_mode == 'local':
                        self._start_local_game()
                    elif self.game_mode == 'online':
                        self._start_online_game()
        
        self.menu_view.render_menu('Select Theme', theme_names, self.selected_menu_option)

    def _start_single_game(self):
        """Start single player game"""
        print(f"\n🎮 Starting Single Player mode for {self.current_user.username}...")
        print(f"   Theme: {self.selected_theme}")
        self.controller = GameController(
            player1_name=self.current_user.username,
            player2_name="AI",
            theme=self.selected_theme,
            is_multiplayer=False
        )
        self.current_screen = 'game'

    def _start_local_game(self):
        """Start local multiplayer game"""
        print("\n🎮 Starting Local Multiplayer mode...")
        print(f"   Theme: {self.selected_theme}")
        self.controller = GameController(
            player1_name="Player 1",
            player2_name="Player 2",
            theme=self.selected_theme,
            is_multiplayer=False
        )
        self.current_screen = 'game'

    def _start_online_game(self):
        """Start online multiplayer game"""
        print(f"\n🌐 Starting Online Multiplayer for {self.current_user.username}...")

        try:
            self.controller = NetworkGameController(
                username=self.current_user.username,
                host=SERVER_HOST,
                port=SERVER_PORT
            )
            self.current_screen = 'waiting'
        except Exception as e:
            print(f"❌ Connection error: {e}")
            self.menu_view.render_connection_error()
            pygame.time.wait(3000)
            self.current_screen = 'main_menu'

    def _handle_waiting(self):
        """Handle waiting for opponent"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if hasattr(self.controller, 'disconnect'):
                        self.controller.disconnect()
                    self.current_screen = 'main_menu'

        # Check if game started
        if hasattr(self.controller, 'network_ready') and self.controller.network_ready:
            self.current_screen = 'game'
        else:
            self.menu_view.render_waiting("Waiting for opponent")

    def _handle_game(self, dt):
        """Handle game screen"""
        # Controller can become None right after a game ends; bail out safely
        if self.controller is None:
            self.current_screen = 'main_menu'
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.controller.game_over:
                        self._end_game()
                    else:
                        if self.controller.paused:
                            self.controller.resume()
                        else:
                            self.controller.pause()

                if event.key == pygame.K_r and self.controller.game_over:
                    self._restart_game()

                # Player 1 bomb (only if not paused)
                if not self.controller.paused and event.key == self.controller.player1_controls['bomb']:
                    self.controller.handle_input(1, 0, 0, place_bomb=True)

                # Player 2 bomb (only if not paused and a second player exists)
                if not self.controller.paused and len(self.controller.players) > 1 and event.key == self.controller.player2_controls['bomb']:
                    if not isinstance(self.controller, NetworkGameController) or \
                            self.controller.my_player_number == 2:
                        self.controller.handle_input(2, 0, 0, place_bomb=True)

        # Handle movement (only if not paused)
        if not self.controller.paused:
            keys = pygame.key.get_pressed()

            # Player 1
            dx1 = dy1 = 0
            if keys[self.controller.player1_controls['left']]:
                dx1 = -1
            if keys[self.controller.player1_controls['right']]:
                dx1 = 1
            if keys[self.controller.player1_controls['up']]:
                dy1 = -1
            if keys[self.controller.player1_controls['down']]:
                dy1 = 1

            if dx1 != 0 or dy1 != 0:
                self.controller.handle_input(1, dx1, dy1)

            # Player 2 (only if a second player exists and we control it)
            if len(self.controller.players) > 1 and (not isinstance(self.controller, NetworkGameController) or \
                    self.controller.my_player_number == 2):
                dx2 = dy2 = 0
                if keys[self.controller.player2_controls['left']]:
                    dx2 = -1
                if keys[self.controller.player2_controls['right']]:
                    dx2 = 1
                if keys[self.controller.player2_controls['up']]:
                    dy2 = -1
                if keys[self.controller.player2_controls['down']]:
                    dy2 = 1

                if dx2 != 0 or dy2 != 0:
                    self.controller.handle_input(2, dx2, dy2)

        # Update and render
        self.controller.update(dt)
        game_state = self.controller.get_game_state()
        self.game_view.render(game_state)

    def _handle_leaderboard(self):
        """Handle leaderboard screen"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.current_screen = 'main_menu'

        # Get leaderboard data
        leaderboard = self.game_repo.get_leaderboard(10)
        self.leaderboard_view.render(leaderboard)

    def _end_game(self):
        """End game and save statistics"""
        if self.current_user and self.controller.winner:
            # Update stats
            won = self.controller.winner.name == self.current_user.username
            self.game_repo.update_stats(self.current_user.user_id, won)

            # Save score
            score = self.controller.score_observer.score
            self.game_repo.add_score(self.current_user.user_id, score)

        # Disconnect if online
        if isinstance(self.controller, NetworkGameController):
            self.controller.disconnect()

        self.controller = None
        self.current_screen = 'main_menu'

    def _restart_game(self):
        """Restart current game"""
        if self.game_mode == 'single':
            self._start_single_game()
        elif self.game_mode == 'local':
            self._start_local_game()
        elif self.game_mode == 'online':
            self._start_online_game()


def main():
    """Main entry point"""
    game = BombermanGame()
    game.run()


if __name__ == "__main__":
    main()