# test_enemies.py
"""
Test enemy AI system with Strategy Pattern
"""

import pygame
from patterns.creational.factory import WallFactory
from patterns.behavioral.strategy import create_ai_strategy
from patterns.behavioral.observer import GameEventManager, GameEvent, ScoreObserver, StatisticsObserver
from models.player import Player
from models.enemy import Enemy
from models.bomb import Bomb, Explosion
from config import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bomberman - Enemy AI Test")
clock = pygame.time.Clock()

# Setup Event Manager
event_manager = GameEventManager()
score_observer = ScoreObserver()
stats_observer = StatisticsObserver()

event_manager.attach(score_observer)
event_manager.attach(stats_observer)

print("✅ Strategy Pattern Test initialized")

# Create walls (border + some obstacles)
walls = []

# Border walls (unbreakable)
for x in range(GRID_WIDTH):
    walls.append(WallFactory.create_wall('unbreakable', x, 0, 'city'))
    walls.append(WallFactory.create_wall('unbreakable', x, GRID_HEIGHT - 1, 'city'))

for y in range(1, GRID_HEIGHT - 1):
    walls.append(WallFactory.create_wall('unbreakable', 0, y, 'city'))
    walls.append(WallFactory.create_wall('unbreakable', GRID_WIDTH - 1, y, 'city'))

# Some internal walls
for x in range(2, GRID_WIDTH - 2, 2):
    for y in range(2, GRID_HEIGHT - 2, 2):
        walls.append(WallFactory.create_wall('unbreakable', x, y, 'city'))

# Some breakable walls
import random

for _ in range(15):
    x = random.randint(2, GRID_WIDTH - 3)
    y = random.randint(2, GRID_HEIGHT - 3)
    if (x, y) not in [(1, 1), (1, 2), (2, 1)]:  # Don't block player spawn
        walls.append(WallFactory.create_wall('breakable', x, y, 'desert'))

# Create player
player1_controls = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'bomb': pygame.K_SPACE
}
player1 = Player(1, 1, 1, RED, player1_controls)
players = [player1]

# Create enemies with different AI strategies
enemies = [
    Enemy(1, 13, 1, (128, 0, 128), create_ai_strategy('static')),  # Purple - Static
    Enemy(2, 13, 11, (255, 0, 255), create_ai_strategy('chasing')),  # Magenta - Chasing
    Enemy(3, 1, 11, (255, 165, 0), create_ai_strategy('intelligent')),  # Orange - Intelligent (A*)
]

print(f"\n✅ Created {len(enemies)} enemies:")
print("  1. Purple (S) - Static AI")
print("  2. Magenta (C) - Chasing AI")
print("  3. Orange (I) - Intelligent AI (A* Pathfinding - BONUS)")

bombs = []
explosions = []

print("\nControls:")
print("  WASD - Move Player")
print("  SPACE - Place Bomb")
print("  1/2/3 - Change Enemy 1/2/3 strategy")
print("  ESC - Exit")

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
                                                {'player': player1.player_id})

            # Change enemy strategies (for testing)
            if event.key == pygame.K_1:
                current = enemies[0].ai_strategy.__class__.__name__
                if 'Static' in current:
                    enemies[0].set_strategy(create_ai_strategy('chasing'))
                elif 'Chasing' in current:
                    enemies[0].set_strategy(create_ai_strategy('intelligent'))
                else:
                    enemies[0].set_strategy(create_ai_strategy('static'))

            if event.key == pygame.K_2 and len(enemies) > 1:
                current = enemies[1].ai_strategy.__class__.__name__
                if 'Static' in current:
                    enemies[1].set_strategy(create_ai_strategy('chasing'))
                elif 'Chasing' in current:
                    enemies[1].set_strategy(create_ai_strategy('intelligent'))
                else:
                    enemies[1].set_strategy(create_ai_strategy('static'))

            if event.key == pygame.K_3 and len(enemies) > 2:
                current = enemies[2].ai_strategy.__class__.__name__
                if 'Static' in current:
                    enemies[2].set_strategy(create_ai_strategy('chasing'))
                elif 'Chasing' in current:
                    enemies[2].set_strategy(create_ai_strategy('intelligent'))
                else:
                    enemies[2].set_strategy(create_ai_strategy('static'))

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

    # Update enemies
    for enemy in enemies:
        enemy.update(dt, walls, players, enemies)

        # Check collision with player
        if enemy.alive and player1.alive and enemy.rect.colliderect(player1.rect):
            player1.die()
            event_manager.trigger_event(GameEvent.PLAYER_DIED, {'player': player1.player_id})
            print("💀 Player killed by enemy!")

    # Update bombs
    for bomb in bombs[:]:
        if bomb.update(dt):
            bombs.remove(bomb)
            player1.bomb_exploded()
            event_manager.trigger_event(GameEvent.BOMB_EXPLODED,
                                        {'position': (bomb.grid_x, bomb.grid_y)})

            # Create explosions
            explosions.append(Explosion(bomb.grid_x, bomb.grid_y, None))

            # Check explosion in 4 directions
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in directions:
                for i in range(1, bomb.power + 1):
                    check_x = bomb.grid_x + (dx * i)
                    check_y = bomb.grid_y + (dy * i)

                    blocked = False

                    # Check walls
                    for wall in walls:
                        if wall.grid_x == check_x and wall.grid_y == check_y:
                            if not wall.destroyed:
                                explosions.append(Explosion(check_x, check_y,
                                                            'right' if dx > 0 else 'left' if dx < 0 else
                                                            'down' if dy > 0 else 'up'))
                                if wall.take_damage():
                                    event_manager.trigger_event(GameEvent.WALL_DESTROYED,
                                                                {'type': wall.get_type()})
                                blocked = True
                                break

                    if blocked:
                        break

                    explosions.append(Explosion(check_x, check_y,
                                                'right' if dx > 0 else 'left' if dx < 0 else
                                                'down' if dy > 0 else 'up'))

                    # Check enemies
                    for enemy in enemies:
                        if enemy.alive and enemy.grid_x == check_x and enemy.grid_y == check_y:
                            enemy.die()
                            event_manager.trigger_event(GameEvent.ENEMY_DIED,
                                                        {'enemy_id': enemy.enemy_id})
                            print(f"💥 Enemy {enemy.enemy_id} killed!")

                    # Check player
                    if player1.alive and player1.grid_x == check_x and player1.grid_y == check_y:
                        player1.die()
                        event_manager.trigger_event(GameEvent.PLAYER_DIED,
                                                    {'player': player1.player_id})
                        print("💀 Player killed by explosion!")

    # Update explosions
    for explosion in explosions[:]:
        if explosion.update(dt):
            explosions.remove(explosion)

    # Drawing
    screen.fill((50, 50, 50))

    # Draw walls
    for wall in walls:
        if not wall.destroyed:
            wall.draw(screen)

    # Draw explosions
    for explosion in explosions:
        explosion.draw(screen)

    # Draw bombs
    for bomb in bombs:
        bomb.draw(screen)

    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)

    # Draw player
    player1.draw(screen)

    # Draw UI
    font = pygame.font.Font(None, 20)
    ui_texts = [
        f"Player: {'ALIVE' if player1.alive else 'DEAD'} | Pos: ({player1.grid_x}, {player1.grid_y})",
        f"Bombs: {player1.bombs_placed}/{player1.bomb_count} | Power: {player1.bomb_power}",
        f"Score: {score_observer.score}",
        "",
        "Enemies:",
    ]

    for i, enemy in enumerate(enemies):
        status = "ALIVE" if enemy.alive else "DEAD"
        ai_type = enemy.ai_strategy.__class__.__name__.replace('AIStrategy', '')
        ui_texts.append(f"  {i + 1}. {ai_type}: {status}")

    for i, text in enumerate(ui_texts):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, 10 + i * 22))

    pygame.display.flip()

pygame.quit()

# Print final statistics
print("\n" + "=" * 50)
stats_observer.print_stats()
print(f"\nFinal Score: {score_observer.score}")
print(f"Player Status: {'Survived' if player1.alive else 'Died'}")
alive_enemies = sum(1 for e in enemies if e.alive)
print(f"Enemies Remaining: {alive_enemies}/{len(enemies)}")
print("=" * 50)
print("\n✅ Strategy Pattern test completed!")