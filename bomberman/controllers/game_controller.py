# controllers/game_controller.py
"""
MVC Pattern - Game Controller
Controls game logic and coordinates between Model and View
"""

import pygame
import random
from patterns.creational.factory import WallFactory, PowerUpFactory
from patterns.behavioral.strategy import create_ai_strategy
from patterns.behavioral.observer import GameEventManager, GameEvent, ScoreObserver, StatisticsObserver
from models.player import Player
from models.enemy import Enemy
from models.bomb import Bomb, Explosion
from config import *


class GameController:
    """
    Main game controller following MVC pattern.
    Manages game state, logic, and coordinates between models and views.
    """

    def __init__(self, player1_name="Player1", player2_name="Player2", theme='desert', is_multiplayer=False):
        """
        Initialize game controller.

        Args:
            player1_name (str): Name of player 1
            player2_name (str): Name of player 2
            theme (str): Game theme
            is_multiplayer (bool): True for online multiplayer
        """
        # Game state
        self.running = False
        self.paused = False
        self.game_over = False
        self.winner = None
        self.winner_label = None
        self.is_multiplayer = is_multiplayer
        # Single-player means only one controllable player; second slot is unused
        self.is_single_player = (not is_multiplayer) and (player2_name == "AI")
        self.theme = theme

        # Event Manager (Observer Pattern)
        self.event_manager = GameEventManager()
        self.score_observer = ScoreObserver()
        self.stats_observer = StatisticsObserver()

        # Import SoundObserver with updated implementation
        from patterns.behavioral.observer import SoundObserver
        self.sound_observer = SoundObserver()

        self.event_manager.attach(self.score_observer)
        self.event_manager.attach(self.stats_observer)
        self.event_manager.attach(self.sound_observer)

        # Game objects
        self.walls = []
        self.players = []
        self.enemies = []
        self.bombs = []
        self.explosions = []
        self.powerups = []

        # Player controls
        self.player1_controls = {
            'up': pygame.K_w,
            'down': pygame.K_s,
            'left': pygame.K_a,
            'right': pygame.K_d,
            'bomb': pygame.K_SPACE
        }

        self.player2_controls = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'bomb': pygame.K_RETURN
        }

        # Initialize game
        self._initialize_game(player1_name, player2_name)

    def _initialize_game(self, player1_name, player2_name):
        """Initialize game objects"""
        print(f"\n🎮 Initializing game: {player1_name} vs {player2_name}")
        print(f"   Theme: {self.theme}")
        print(f"   Multiplayer: {self.is_multiplayer}")

        # Create map
        self._create_map()

        # Create players
        player1 = Player(1, 1, 1, RED, self.player1_controls)
        player1.name = player1_name
        self.players.append(player1)

        if not self.is_single_player:
            player2 = Player(2, GRID_WIDTH - 2, GRID_HEIGHT - 2, BLUE, self.player2_controls)
            player2.name = player2_name
            self.players.append(player2)
            print(f"   ✓ Players created")
        else:
            print(f"   ✓ Player created (single-player)")

        # Create enemies (for single player or practice)
        if not self.is_multiplayer:
            self._create_enemies()

        self.running = True
        print(f"   ✓ Game initialized!\n")

    def _create_map(self):
        """Create game map with walls"""
        # Border walls (unbreakable)
        for x in range(GRID_WIDTH):
            self.walls.append(WallFactory.create_wall('unbreakable', x, 0, self.theme))
            self.walls.append(WallFactory.create_wall('unbreakable', x, GRID_HEIGHT - 1, self.theme))

        for y in range(1, GRID_HEIGHT - 1):
            self.walls.append(WallFactory.create_wall('unbreakable', 0, y, self.theme))
            self.walls.append(WallFactory.create_wall('unbreakable', GRID_WIDTH - 1, y, self.theme))

        # Internal unbreakable walls (grid pattern)
        for x in range(2, GRID_WIDTH - 2, 2):
            for y in range(2, GRID_HEIGHT - 2, 2):
                self.walls.append(WallFactory.create_wall('unbreakable', x, y, self.theme))

        # Random breakable and hard walls
        safe_positions = [(1, 1), (1, 2), (2, 1),
                          (GRID_WIDTH - 2, GRID_HEIGHT - 2),
                          (GRID_WIDTH - 2, GRID_HEIGHT - 3),
                          (GRID_WIDTH - 3, GRID_HEIGHT - 2)]

        for _ in range(30):
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)

            if (x, y) not in safe_positions:
                # Check if position is already occupied
                occupied = False
                for wall in self.walls:
                    if wall.grid_x == x and wall.grid_y == y:
                        occupied = True
                        break

                if not occupied:
                    wall_type = random.choice(['breakable', 'breakable', 'hard'])
                    self.walls.append(WallFactory.create_wall(wall_type, x, y, self.theme))

        # Add initial power-ups at specific strategic locations
        initial_powerup_positions = [
            (3, 4, 'speed_boost'),
            (5, 3, 'bomb_count'),
            (GRID_WIDTH - 4, 4, 'bomb_power'),
            (3, GRID_HEIGHT - 4, 'bomb_count'),
            (GRID_WIDTH - 4, GRID_HEIGHT - 4, 'speed_boost'),
        ]
        
        for x, y, ptype in initial_powerup_positions:
            # Check if position is safe (no walls)
            occupied = False
            for wall in self.walls:
                if wall.grid_x == x and wall.grid_y == y:
                    occupied = True
                    break
            if not occupied:
                powerup = PowerUpFactory.create_powerup(ptype, x, y)
                self.powerups.append(powerup)

        print(f"   ✓ Map created with {len(self.walls)} walls and {len(self.powerups)} initial powerups")

    def _create_enemies(self):
        """Create enemy NPCs"""
        enemy_positions = [
            (GRID_WIDTH // 2, 1),
            (GRID_WIDTH - 3, GRID_HEIGHT // 2),
            (3, GRID_HEIGHT - 3)
        ]

        ai_types = ['static', 'chasing', 'intelligent']
        colors = [(128, 0, 128), (255, 0, 255), (255, 165, 0)]

        for i, (pos, ai_type, color) in enumerate(zip(enemy_positions, ai_types, colors)):
            enemy = Enemy(i + 1, pos[0], pos[1], color, create_ai_strategy(ai_type))
            self.enemies.append(enemy)

        print(f"   ✓ Created {len(self.enemies)} enemies")

    def update(self, dt):
        """
        Update game state.

        Args:
            dt (int): Delta time in milliseconds
        """
        if not self.running or self.paused or self.game_over:
            return

        # Update players
        for player in self.players:
            if hasattr(player, 'state_manager'):
                player.state_manager.update(dt)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(dt, self.walls, self.players, self.enemies)

            # Check collision with players
            for player in self.players:
                if enemy.alive and player.state_manager.is_alive() and enemy.rect.colliderect(player.rect):
                    player.die()
                    self.event_manager.trigger_event(GameEvent.PLAYER_DIED,
                                                     {'player': player.player_id})
            
            # Remove dead enemies from list
            if not enemy.alive:
                self.enemies.remove(enemy)

        # Update bombs
        for bomb in self.bombs[:]:
            if bomb.update(dt):
                self._handle_bomb_explosion(bomb)
                self.bombs.remove(bomb)
                bomb.owner.bomb_exploded()

        # Update explosions
        for explosion in self.explosions[:]:
            if explosion.update(dt):
                self.explosions.remove(explosion)

        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update(dt)

            # Check collision with players
            for player in self.players:
                if player.state_manager.is_alive() and player.rect.colliderect(powerup.rect) and not powerup.collected:
                    powerup.collected = True
                    powerup.apply(player)
                    self.powerups.remove(powerup)
                    self.event_manager.trigger_event(GameEvent.POWERUP_COLLECTED,
                                                     {'type': powerup.name,
                                                      'player': player.player_id})

        # Check game over
        self._check_game_over()

    def handle_input(self, player_id, dx, dy, place_bomb=False):
        """
        Handle player input.

        Args:
            player_id (int): Player ID (1 or 2)
            dx (int): X direction
            dy (int): Y direction
            place_bomb (bool): True to place bomb
        """
        if self.game_over:
            return

        player = self.players[player_id - 1]

        if not player.state_manager.is_alive():
            return

        # Movement
        if dx != 0 or dy != 0:
            player.move(dx, dy, self.walls)

        # Place bomb
        if place_bomb and player.can_place_bomb():
            bomb = Bomb(player.grid_x, player.grid_y, player.bomb_power, player)
            self.bombs.append(bomb)
            player.place_bomb()
            self.event_manager.trigger_event(GameEvent.BOMB_PLACED,
                                             {'player': player.player_id,
                                              'position': (player.grid_x, player.grid_y)})

    def _handle_bomb_explosion(self, bomb):
        """Handle bomb explosion effects"""
        self.event_manager.trigger_event(GameEvent.BOMB_EXPLODED,
                                         {'position': (bomb.grid_x, bomb.grid_y),
                                          'power': bomb.power})

        # Center explosion
        self.explosions.append(Explosion(bomb.grid_x, bomb.grid_y, None))
        self._check_explosion_damage(bomb.grid_x, bomb.grid_y)

        # Directional explosions
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        direction_names = ['up', 'down', 'left', 'right']

        for (dx, dy), dir_name in zip(directions, direction_names):
            for i in range(1, bomb.power + 1):
                check_x = bomb.grid_x + (dx * i)
                check_y = bomb.grid_y + (dy * i)

                # Check boundaries
                if check_x < 0 or check_x >= GRID_WIDTH or check_y < 0 or check_y >= GRID_HEIGHT:
                    break

                blocked = False

                # Check walls
                for wall in self.walls:
                    if wall.grid_x == check_x and wall.grid_y == check_y and not wall.destroyed:
                        self.explosions.append(Explosion(check_x, check_y, dir_name))

                        if wall.take_damage():
                            self.event_manager.trigger_event(GameEvent.WALL_DESTROYED,
                                                             {'type': wall.get_type(),
                                                              'position': (check_x, check_y)})

                            # Spawn powerup
                            if wall.get_type() == 'breakable' and random.random() < POWERUP_SPAWN_CHANCE:
                                powerup_type = random.choice(POWERUP_TYPES)
                                powerup = PowerUpFactory.create_powerup(powerup_type, check_x, check_y)
                                self.powerups.append(powerup)
                                self.event_manager.trigger_event(GameEvent.POWERUP_SPAWNED,
                                                                 {'type': powerup_type,
                                                                  'position': (check_x, check_y)})

                        blocked = True
                        break

                if blocked:
                    break

                self.explosions.append(Explosion(check_x, check_y, dir_name))
                self._check_explosion_damage(check_x, check_y)

    def _check_explosion_damage(self, x, y):
        """Check if explosion damages players or enemies"""
        # Check players
        for player in self.players:
            if player.state_manager.is_alive() and player.grid_x == x and player.grid_y == y:
                player.die()
                self.event_manager.trigger_event(GameEvent.PLAYER_DIED,
                                                 {'player': player.player_id})

        # Check enemies
        for enemy in self.enemies:
            if enemy.alive and enemy.grid_x == x and enemy.grid_y == y:
                enemy.die()
                self.event_manager.trigger_event(GameEvent.ENEMY_DIED,
                                                 {'enemy_id': enemy.enemy_id})

    def _check_game_over(self):
        """Check if game is over"""
        # Single-player: win when all enemies die; lose when the only player dies
        if self.is_single_player:
            player = self.players[0]
            alive_enemies = [e for e in self.enemies if e.alive]

            if not player.state_manager.is_alive():
                self.game_over = True
                self.winner = None
                self.winner_label = "AI"
                print("💀 Game Over: You died! AI wins!")
            elif len(alive_enemies) == 0:
                self.game_over = True
                self.winner = player
                self.winner_label = player.name
                self.event_manager.trigger_event(GameEvent.GAME_WON,
                                                 {'player': self.winner.player_id})
                print(f"🏆 Game Over: {self.winner.name} wins!")
            return

        # Local/online multiplayer logic
        alive_players = [p for p in self.players if p.state_manager.is_alive()]

        if len(alive_players) == 0:
            # Both dead - draw
            self.game_over = True
            self.winner = None
            self.winner_label = "DRAW"
            print("💀 Game Over: Draw!")
        elif len(alive_players) == 1:
            # One winner
            self.game_over = True
            self.winner = alive_players[0]
            self.winner_label = self.winner.name
            self.event_manager.trigger_event(GameEvent.GAME_WON,
                                             {'player': self.winner.player_id})
            print(f"🏆 Game Over: {self.winner.name} wins!")

    def pause(self):
        """Pause the game"""
        self.paused = True

    def resume(self):
        """Resume the game"""
        self.paused = False

    def get_game_state(self):
        """Get current game state for rendering"""
        return {
            'walls': self.walls,
            'players': self.players,
            'enemies': self.enemies,
            'bombs': self.bombs,
            'explosions': self.explosions,
            'powerups': self.powerups,
            'score': self.score_observer.score,
            'stats': self.stats_observer.stats,
            'game_over': self.game_over,
            'winner': self.winner,
            'is_single_player': self.is_single_player,
            'winner_label': self.winner_label
        }