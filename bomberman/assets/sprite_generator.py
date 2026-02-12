# assets/sprite_generator.py
"""
Generate beautiful sprites for the game using procedural graphics
"""

import pygame
import math
import os


def create_gradient_circle(size, color1, color2):
    """Create a circle with radial gradient"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2

    for radius in range(center, 0, -1):
        # Interpolate between colors
        t = radius / center
        r = int(color1[0] * t + color2[0] * (1 - t))
        g = int(color1[1] * t + color2[1] * (1 - t))
        b = int(color1[2] * t + color2[2] * (1 - t))

        pygame.draw.circle(surface, (r, g, b), (center, center), radius)

    return surface


def create_player_sprite(size, base_color, player_num):
    """Create an animated player sprite with face"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2

    # Body (gradient circle)
    for radius in range(center - 2, center // 3, -1):
        t = (radius - center // 3) / (center - 2 - center // 3)
        # Darken towards center
        r = int(base_color[0] * (0.7 + 0.3 * t))
        g = int(base_color[1] * (0.7 + 0.3 * t))
        b = int(base_color[2] * (0.7 + 0.3 * t))
        pygame.draw.circle(surface, (r, g, b), (center, center), radius)

    # Outline
    pygame.draw.circle(surface, (0, 0, 0), (center, center), center - 2, 2)

    # Eyes
    eye_y = center - 3
    if player_num == 1:
        # Player 1 - happy eyes
        pygame.draw.circle(surface, (255, 255, 255), (center - 5, eye_y), 3)
        pygame.draw.circle(surface, (255, 255, 255), (center + 5, eye_y), 3)
        pygame.draw.circle(surface, (0, 0, 0), (center - 5, eye_y), 2)
        pygame.draw.circle(surface, (0, 0, 0), (center + 5, eye_y), 2)
    else:
        # Player 2 - determined eyes
        pygame.draw.circle(surface, (255, 255, 255), (center - 5, eye_y), 3)
        pygame.draw.circle(surface, (255, 255, 255), (center + 5, eye_y), 3)
        pygame.draw.circle(surface, (0, 0, 0), (center - 5, eye_y + 1), 2)
        pygame.draw.circle(surface, (0, 0, 0), (center + 5, eye_y + 1), 2)

    # Mouth (smile)
    mouth_rect = pygame.Rect(center - 8, center + 2, 16, 8)
    pygame.draw.arc(surface, (0, 0, 0), mouth_rect, 0, math.pi, 2)

    # Player number badge
    font = pygame.font.Font(None, 16)
    text = font.render(f"P{player_num}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(center, size - 8))

    # Badge background
    badge_rect = pygame.Rect(text_rect.x - 2, text_rect.y - 1, text_rect.width + 4, text_rect.height + 2)
    pygame.draw.rect(surface, (0, 0, 0, 180), badge_rect, border_radius=3)

    surface.blit(text, text_rect)

    return surface


def create_bomb_sprite(size):
    """Create an animated bomb sprite"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2

    # Bomb body (black with gradient)
    for radius in range(center - 2, center // 4, -1):
        t = (radius - center // 4) / (center - 2 - center // 4)
        brightness = int(80 * t)
        pygame.draw.circle(surface, (brightness, brightness, brightness), (center, center), radius)

    # Highlight
    pygame.draw.circle(surface, (120, 120, 120), (center - 4, center - 4), 3)

    # Fuse
    fuse_points = [
        (center, center - (center - 2)),
        (center - 2, center - (center - 2) - 5),
        (center, center - (center - 2) - 8)
    ]
    pygame.draw.lines(surface, (139, 69, 19), False, fuse_points, 2)

    # Spark at fuse tip
    pygame.draw.circle(surface, (255, 200, 0), fuse_points[-1], 2)

    return surface


def create_powerup_sprite(size, powerup_type):
    """Create power-up sprites with icons"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2

    # Color map
    colors = {
        'bomb_count': ((255, 0, 0), (255, 100, 100)),
        'bomb_power': ((255, 165, 0), (255, 200, 100)),
        'speed_boost': ((0, 255, 0), (100, 255, 100)),
        'skateboard': ((0, 255, 255), (100, 255, 255)),
        'wall_pass': ((255, 255, 0), (255, 255, 150))
    }

    color1, color2 = colors.get(powerup_type, ((255, 255, 255), (200, 200, 200)))

    # Rotating star background
    star_points = []
    for i in range(8):
        angle = (i * math.pi / 4)
        radius = (center - 2) if i % 2 == 0 else (center - 8)
        x = center + int(radius * math.cos(angle))
        y = center + int(radius * math.sin(angle))
        star_points.append((x, y))

    # Gradient fill
    pygame.draw.polygon(surface, color1, star_points)

    # Inner star
    inner_points = []
    for i in range(8):
        angle = (i * math.pi / 4) + (math.pi / 8)
        radius = (center - 6) if i % 2 == 0 else (center - 10)
        x = center + int(radius * math.cos(angle))
        y = center + int(radius * math.sin(angle))
        inner_points.append((x, y))

    pygame.draw.polygon(surface, color2, inner_points)

    # Icon
    font = pygame.font.Font(None, 20)
    icons = {
        'bomb_count': 'B',
        'bomb_power': 'P',
        'speed_boost': 'S',
        'skateboard': 'SK',
        'wall_pass': 'W'
    }

    icon = icons.get(powerup_type, '?')
    text = font.render(icon, True, (255, 255, 255))
    text_rect = text.get_rect(center=(center, center))

    # Shadow
    shadow = font.render(icon, True, (0, 0, 0))
    surface.blit(shadow, (text_rect.x + 1, text_rect.y + 1))
    surface.blit(text, text_rect)

    return surface


def create_enemy_sprite(size, enemy_type):
    """Create enemy sprites with different looks"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2

    # Color and style based on type
    if enemy_type == 'static':
        base_color = (128, 0, 128)  # Purple
        eye_color = (255, 0, 0)
    elif enemy_type == 'chasing':
        base_color = (255, 0, 255)  # Magenta
        eye_color = (255, 100, 0)
    else:  # intelligent
        base_color = (255, 165, 0)  # Orange
        eye_color = (255, 0, 0)

    # Body (darker gradient)
    for radius in range(center - 2, center // 3, -1):
        t = (radius - center // 3) / (center - 2 - center // 3)
        r = int(base_color[0] * (0.5 + 0.5 * t))
        g = int(base_color[1] * (0.5 + 0.5 * t))
        b = int(base_color[2] * (0.5 + 0.5 * t))
        pygame.draw.circle(surface, (r, g, b), (center, center), radius)

    # Spiky outline
    pygame.draw.circle(surface, (0, 0, 0), (center, center), center - 2, 2)

    # Evil eyes
    pygame.draw.circle(surface, (0, 0, 0), (center - 6, center - 4), 4)
    pygame.draw.circle(surface, (0, 0, 0), (center + 6, center - 4), 4)
    pygame.draw.circle(surface, eye_color, (center - 6, center - 4), 2)
    pygame.draw.circle(surface, eye_color, (center + 6, center - 4), 2)

    # Evil grin
    mouth_points = [
        (center - 8, center + 4),
        (center - 4, center + 6),
        (center, center + 5),
        (center + 4, center + 6),
        (center + 8, center + 4)
    ]
    pygame.draw.lines(surface, (0, 0, 0), False, mouth_points, 2)

    # Type indicator
    font = pygame.font.Font(None, 14)
    type_chars = {'static': 'S', 'chasing': 'C', 'intelligent': 'A*'}
    text = font.render(type_chars.get(enemy_type, '?'), True, (255, 255, 255))
    text_rect = text.get_rect(center=(center, size - 6))
    surface.blit(text, text_rect)

    return surface


def create_wall_sprite(size, wall_type, theme='desert'):
    """Create wall sprites with textures"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    # Theme colors
    theme_colors = {
        'desert': {
            'unbreakable': ((139, 69, 19), (101, 67, 33)),
            'breakable': ((160, 82, 45), (205, 133, 63)),
            'hard': ((205, 133, 63), (244, 164, 96))
        },
        'forest': {
            'unbreakable': ((47, 79, 47), (34, 139, 34)),
            'breakable': ((0, 100, 0), (34, 139, 34)),
            'hard': ((85, 107, 47), (107, 142, 35))
        },
        'city': {
            'unbreakable': ((105, 105, 105), (128, 128, 128)),
            'breakable': ((169, 169, 169), (192, 192, 192)),
            'hard': ((112, 128, 144), (119, 136, 153))
        }
    }

    color1, color2 = theme_colors[theme][wall_type]

    # Base
    surface.fill(color1)

    # Texture pattern
    if wall_type == 'unbreakable':
        # Grid pattern
        for i in range(0, size, size // 4):
            pygame.draw.line(surface, color2, (i, 0), (i, size), 1)
            pygame.draw.line(surface, color2, (0, i), (size, i), 1)
    elif wall_type == 'breakable':
        # Brick pattern
        brick_height = size // 3
        for row in range(3):
            offset = 0 if row % 2 == 0 else size // 2
            y = row * brick_height
            for col in range(3):
                x = col * size // 2 + offset
                if x < size:
                    rect = pygame.Rect(x, y, size // 2 - 2, brick_height - 2)
                    pygame.draw.rect(surface, color2, rect)
    else:  # hard
        # Reinforced pattern
        pygame.draw.rect(surface, color2, (2, 2, size - 4, size - 4), 3)
        pygame.draw.line(surface, color2, (size // 2, 2), (size // 2, size - 2), 2)
        pygame.draw.line(surface, color2, (2, size // 2), (size - 2, size // 2), 2)

    # Border
    pygame.draw.rect(surface, (0, 0, 0), (0, 0, size, size), 1)

    return surface


def create_explosion_frame(size, frame, total_frames):
    """Create explosion animation frame"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2

    # Animation progress (0 to 1)
    progress = frame / total_frames

    # Expanding radius
    max_radius = center
    radius = int(max_radius * progress)

    # Colors fade from yellow to red to transparent
    if progress < 0.3:
        color = (255, 255, 0, 255)  # Yellow
    elif progress < 0.6:
        t = (progress - 0.3) / 0.3
        r = 255
        g = int(255 * (1 - t))
        b = 0
        color = (r, g, b, 255)  # Yellow to red
    else:
        t = (progress - 0.6) / 0.4
        alpha = int(255 * (1 - t))
        color = (255, 0, 0, alpha)  # Fading red

    # Draw expanding circle
    pygame.draw.circle(surface, color, (center, center), radius)

    # Inner bright core
    if progress < 0.5:
        core_radius = max(2, int(radius * 0.3))
        pygame.draw.circle(surface, (255, 255, 255), (center, center), core_radius)

    return surface


def main():
    """Generate all game sprites"""
    pygame.init()

    print("=" * 60)
    print("🎨 SPRITE GENERATOR")
    print("=" * 60 + "\n")

    # Create directories
    os.makedirs('assets/images/players', exist_ok=True)
    os.makedirs('assets/images/bombs', exist_ok=True)
    os.makedirs('assets/images/powerups', exist_ok=True)
    os.makedirs('assets/images/enemies', exist_ok=True)
    os.makedirs('assets/images/walls', exist_ok=True)
    os.makedirs('assets/images/explosions', exist_ok=True)

    print("Generating sprites...\n")

    # Players
    print("📦 Players:")
    pygame.image.save(create_player_sprite(40, (255, 0, 0), 1), 'assets/images/players/player1.png')
    print("  ✅ player1.png")
    pygame.image.save(create_player_sprite(40, (0, 0, 255), 2), 'assets/images/players/player2.png')
    print("  ✅ player2.png")

    # Bomb
    print("\n💣 Bombs:")
    pygame.image.save(create_bomb_sprite(40), 'assets/images/bombs/bomb.png')
    print("  ✅ bomb.png")

    # Power-ups
    print("\n⭐ Power-ups:")
    for ptype in ['bomb_count', 'bomb_power', 'speed_boost', 'skateboard', 'wall_pass']:
        pygame.image.save(create_powerup_sprite(30, ptype), f'assets/images/powerups/{ptype}.png')
        print(f"  ✅ {ptype}.png")

    # Enemies
    print("\n👾 Enemies:")
    for etype in ['static', 'chasing', 'intelligent']:
        pygame.image.save(create_enemy_sprite(40, etype), f'assets/images/enemies/{etype}.png')
        print(f"  ✅ {etype}.png")

    # Walls
    print("\n🧱 Walls:")
    for theme in ['desert', 'forest', 'city']:
        for wtype in ['unbreakable', 'breakable', 'hard']:
            filename = f'assets/images/walls/{theme}_{wtype}.png'
            pygame.image.save(create_wall_sprite(40, wtype, theme), filename)
            print(f"  ✅ {theme}_{wtype}.png")

    # Explosion frames
    print("\n💥 Explosions:")
    for frame in range(8):
        pygame.image.save(create_explosion_frame(40, frame, 8), f'assets/images/explosions/explosion_{frame}.png')
        print(f"  ✅ explosion_{frame}.png")

    print("\n" + "=" * 60)
    print("✅ All sprites generated successfully!")
    print("\nGenerated files:")
    print("  - 2 player sprites")
    print("  - 1 bomb sprite")
    print("  - 5 power-up sprites")
    print("  - 3 enemy sprites")
    print("  - 9 wall sprites (3 themes × 3 types)")
    print("  - 8 explosion animation frames")
    print("\nTotal: 28 sprite files")
    print("=" * 60)


if __name__ == "__main__":
    main()