# test_powerups.py
"""
Test power-ups, decorator pattern, and observer pattern
"""

import pygame
import random
from patterns.creational.factory import WallFactory, PowerUpFactory
from patterns.behavioral.observer import GameEventManager, GameEvent, ScoreObserver, SoundObserver, StatisticsObserver
from models.player import Player
from models.bomb import Bomb
from config import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bomberman - PowerUp & Observer Test")
clock = pygame.time.Clock()

# Setup Event Manager and Observers
event_manager = GameEventManager()
score_observer = ScoreObserver()
sound_observer = SoundObserver()
stats_observer = StatisticsObserver()

event_manager.attach(score_observer)
event_manager.attach(sound_observer)
event_manager.attach(stats_observer)

print("✅ Observer Pattern initialized")

# Create test walls
walls = []
for i in range(3, 12):
    if i % 2 == 0:
        walls.append(WallFactory.create_wall('breakable', i, 5, 'desert'))
    else:
        walls.append(WallFactory.create_wall('unbreakable', i, 5, 'city'))

# Create player
player1_controls = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'bomb': pygame.K_SPACE
}
player1 = Player(1, 2, 2, RED, player1_controls)

# Create some power-ups to test
powerups = [
    PowerUpFactory.create_powerup('bomb_count', 7, 3),
    PowerUpFactory.create_powerup('bomb_power', 9, 3),
    PowerUpFactory.create_powerup('speed_boost', 11, 3),
]

bombs = []

print("\n✅ Test initialized!")
print("\nControls:")
print("  WASD - Move Player")
print("  SPACE - Place Bomb")
print("  ESC - Exit")
print("\nCollect power-ups to see Decorator Pattern in action!")
print("Destroy walls to see Observer Pattern notifications!\n")

# Game loop
running = True
while running:
    dt = clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # Place bomb
            if event.key == player1.controls['bomb']:
                if player1.can_place_bomb():
                    bomb = Bomb(player1.grid_x, player1.grid_y, player1.bomb_power, player1)
                    bombs.append(bomb)
                    player1.place_bomb()
                    event_manager.trigger_event(GameEvent.BOMB_PLACED,
                                                {'player': player1.player_id,
                                                 'position': (player1.grid_x, player1.grid_y)})

    # Player movement
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[player1.controls['left']]:
        dx = -1
    if keys[player1.controls['right']]:
        dx = 1
    if keys[player1.controls['up']]:
        dy = -1
    if keys[player1.controls['down']]:
        dy = 1

    if dx != 0 or dy != 0:
        player1.move(dx, dy, walls)

    # Update power-ups
    for powerup in powerups[:]:
        powerup.update(dt)
        # Check collision with player
        if player1.rect.colliderect(powerup.rect) and not powerup.collected:
            powerup.collected = True
            powerup.apply(player1)
            powerups.remove(powerup)
            event_manager.trigger_event(GameEvent.POWERUP_COLLECTED,
                                        {'type': powerup.name,
                                         'player': player1.player_id})

    # Update bombs
    for bomb in bombs[:]:
        if bomb.update(dt):
            bombs.remove(bomb)
            player1.bomb_exploded()
            event_manager.trigger_event(GameEvent.BOMB_EXPLODED,
                                        {'position': (bomb.grid_x, bomb.grid_y),
                                         'power': bomb.power})

            # Check wall destruction
            directions = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in directions:
                for i in range(bomb.power):
                    check_x = bomb.grid_x + (dx * i)
                    check_y = bomb.grid_y + (dy * i)

                    for wall in walls:
                        if wall.grid_x == check_x and wall.grid_y == check_y:
                            if wall.take_damage():
                                event_manager.trigger_event(GameEvent.WALL_DESTROYED,
                                                            {'type': wall.get_type(),
                                                             'position': (check_x, check_y)})
                                # Spawn power-up randomly
                                if wall.get_type() == 'breakable' and random.random() < POWERUP_SPAWN_CHANCE:
                                    powerup_type = random.choice(POWERUP_TYPES)
                                    new_powerup = PowerUpFactory.create_powerup(powerup_type, check_x, check_y)
                                    powerups.append(new_powerup)
                                    event_manager.trigger_event(GameEvent.POWERUP_SPAWNED,
                                                                {'type': powerup_type,
                                                                 'position': (check_x, check_y)})

    # Drawing
    screen.fill((100, 100, 100))

    # Draw grid
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, (80, 80, 80), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, (80, 80, 80), (0, y), (SCREEN_WIDTH, y))

    # Draw walls
    for wall in walls:
        if not wall.destroyed:
            wall.draw(screen)

    # Draw power-ups
    for powerup in powerups:
        powerup.draw(screen)

    # Draw bombs
    for bomb in bombs:
        bomb.draw(screen)

    # Draw player
    player1.draw(screen)

    # Draw UI
    font = pygame.font.Font(None, 24)
    ui_texts = [
        f"Position: ({player1.grid_x}, {player1.grid_y})",
        f"Bombs: {player1.bombs_placed}/{player1.bomb_count}",
        f"Power: {player1.bomb_power}",
        f"Speed: {player1.speed}",
        f"",
        f"Score: {score_observer.score}",
    ]

    for i, text in enumerate(ui_texts):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, 10 + i * 25))

    # Draw statistics in top right
    stats_texts = [
        "Statistics:",
        f"Bombs: {stats_observer.stats['bombs_placed']}",
        f"Walls: {stats_observer.stats['walls_destroyed']}",
        f"PowerUps: {stats_observer.stats['powerups_collected']}",
    ]

    for i, text in enumerate(stats_texts):
        text_surface = font.render(text, True, YELLOW)
        screen.blit(text_surface, (SCREEN_WIDTH - 150, 10 + i * 25))

    pygame.display.flip()

pygame.quit()

# Print final statistics
print("\n" + "=" * 50)
stats_observer.print_stats()
print(f"\nFinal Score: {score_observer.score}")
print("=" * 50)
print("\n✅ Test completed!")