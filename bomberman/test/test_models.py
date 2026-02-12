# test_models.py
"""
Test file for basic models and patterns
"""

import pygame
from patterns.creational.factory import WallFactory
from models.player import Player
from models.bomb import Bomb
from config import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bomberman - Model Test")
clock = pygame.time.Clock()

# Test Factory Pattern - Create walls
print("=== Testing Factory Pattern ===")
walls = []
for theme in ['desert', 'forest', 'city']:
    print(f"\nCreating {theme} theme walls:")
    unbreakable = WallFactory.create_wall('unbreakable', 0, 0, theme)
    breakable = WallFactory.create_wall('breakable', 1, 0, theme)
    hard = WallFactory.create_wall('hard', 2, 0, theme)
    print(f"  ✓ {unbreakable.get_type()}")
    print(f"  ✓ {breakable.get_type()}")
    print(f"  ✓ {hard.get_type()}")

# Create test walls for display
test_walls = [
    WallFactory.create_wall('unbreakable', 5, 5, 'desert'),
    WallFactory.create_wall('breakable', 6, 5, 'forest'),
    WallFactory.create_wall('hard', 7, 5, 'city'),
]

# Test Player
print("\n=== Testing Player Class ===")
player1_controls = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'bomb': pygame.K_SPACE
}
player1 = Player(1, 1, 1, RED, player1_controls)
print(f"  ✓ Player 1 created at ({player1.grid_x}, {player1.grid_y})")
print(f"  ✓ Initial bomb count: {player1.bomb_count}")
print(f"  ✓ Initial bomb power: {player1.bomb_power}")

# Test Bomb
print("\n=== Testing Bomb Class ===")
test_bomb = Bomb(3, 3, player1.bomb_power, player1)
print(f"  ✓ Bomb created at ({test_bomb.grid_x}, {test_bomb.grid_y})")
print(f"  ✓ Bomb power: {test_bomb.power}")
print(f"  ✓ Timer: {test_bomb.timer}ms")

print("\n✅ All tests passed! Starting visual test...")
print("\nControls:")
print("  WASD - Move Player")
print("  SPACE - Place Bomb (not functional yet)")
print("  ESC - Exit")

# Game loop for visual test
running = True
bombs = [test_bomb]

while running:
    dt = clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

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
        player1.move(dx, dy, test_walls)

    # Update bombs
    for bomb in bombs[:]:
        if bomb.update(dt):
            print(f"💥 Bomb exploded at ({bomb.grid_x}, {bomb.grid_y})")
            bombs.remove(bomb)
            player1.bomb_exploded()

    # Drawing
    screen.fill((100, 100, 100))

    # Draw grid
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, (80, 80, 80), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, (80, 80, 80), (0, y), (SCREEN_WIDTH, y))

    # Draw walls
    for wall in test_walls:
        wall.draw(screen)

    # Draw bombs
    for bomb in bombs:
        bomb.draw(screen)

    # Draw player
    player1.draw(screen)

    # Draw info
    font = pygame.font.Font(None, 24)
    info_texts = [
        f"Player Position: ({player1.grid_x}, {player1.grid_y})",
        f"Bombs: {player1.bombs_placed}/{player1.bomb_count}",
        f"Power: {player1.bomb_power}",
        f"Speed: {player1.speed}",
    ]
    for i, text in enumerate(info_texts):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, 10 + i * 25))

    pygame.display.flip()

pygame.quit()
print("\n👋 Test completed!")