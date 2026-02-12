# assets/asset_loader.py
"""
Asset Loader - Loads and manages game assets (images, sounds)
Uses Singleton pattern to ensure assets are loaded only once
"""

import pygame
import os
from patterns.creational.singleton import DatabaseConnection


class AssetLoader:
    """
    Singleton class for loading and managing game assets.
    Assets are loaded once and cached for performance.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.images = {}
            self.sounds = {}
            self._load_assets()
            AssetLoader._initialized = True

    def _load_assets(self):
        """Load all game assets"""
        print("📦 Loading assets...")
        self._load_sounds()
        self._create_default_images()
        print("✅ Assets loaded successfully!\n")

    def _load_sounds(self):
        """Load sound effects"""
        try:
            pygame.mixer.init()

            sound_files = {
                'bomb_place': 'assets/sounds/bomb_place.wav',
                'explosion': 'assets/sounds/explosion.wav',
                'powerup': 'assets/sounds/powerup.wav',
                'death': 'assets/sounds/death.wav',
                'wall_break': 'assets/sounds/wall_break.wav'
            }

            for name, path in sound_files.items():
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                    print(f"  ✅ Sound: {name}")
                else:
                    print(f"  ⚠️  Sound not found: {name} (using placeholder)")

        except Exception as e:
            print(f"  ⚠️  Sound system error: {e}")

    def _create_default_images(self):
        """Load sprite images from files"""
        print("  🎨 Loading sprites...")

        # Try to load generated sprites
        sprite_files = {
            # Players
            'player1': 'assets/images/players/player1.png',
            'player2': 'assets/images/players/player2.png',

            # Bomb
            'bomb': 'assets/images/bombs/bomb.png',

            # Power-ups
            'powerup_bomb_count': 'assets/images/powerups/bomb_count.png',
            'powerup_bomb_power': 'assets/images/powerups/bomb_power.png',
            'powerup_speed_boost': 'assets/images/powerups/speed_boost.png',
            'powerup_skateboard': 'assets/images/powerups/skateboard.png',
            'powerup_wall_pass': 'assets/images/powerups/wall_pass.png',

            # Enemies
            'enemy_static': 'assets/images/enemies/static.png',
            'enemy_chasing': 'assets/images/enemies/chasing.png',
            'enemy_intelligent': 'assets/images/enemies/intelligent.png',
        }

        loaded_count = 0
        for name, path in sprite_files.items():
            if os.path.exists(path):
                self.images[name] = pygame.image.load(path).convert_alpha()
                loaded_count += 1
            else:
                # Fallback to simple colored circle
                size = 40 if 'player' in name or 'enemy' in name or 'bomb' in name else 30
                color = self._get_fallback_color(name)
                self.images[name] = self._create_circle_surface(size, color)

        # Load wall sprites for all themes
        for theme in ['desert', 'forest', 'city']:
            for wall_type in ['unbreakable', 'breakable', 'hard']:
                key = f'wall_{theme}_{wall_type}'
                path = f'assets/images/walls/{theme}_{wall_type}.png'
                if os.path.exists(path):
                    self.images[key] = pygame.image.load(path).convert_alpha()
                    loaded_count += 1
                else:
                    self.images[key] = self._create_simple_wall(wall_type, theme)

        # Load explosion animation frames
        self.images['explosion_frames'] = []
        for i in range(8):
            path = f'assets/images/explosions/explosion_{i}.png'
            if os.path.exists(path):
                frame = pygame.image.load(path).convert_alpha()
                self.images['explosion_frames'].append(frame)
                loaded_count += 1
            else:
                # Create simple expanding circle
                frame = self._create_explosion_frame(i)
                self.images['explosion_frames'].append(frame)

        if loaded_count > 0:
            print(f"  ✅ Loaded {loaded_count} sprite files")
        else:
            print(f"  ⚠️  No sprites found, using fallback graphics")

        print(f"  ✅ Total images: {len(self.images)}")

    def _get_fallback_color(self, name):
        """Get fallback color for sprites"""
        color_map = {
            'player1': (255, 0, 0),
            'player2': (0, 0, 255),
            'bomb': (0, 0, 0),
            'powerup_bomb_count': (255, 0, 0),
            'powerup_bomb_power': (255, 165, 0),
            'powerup_speed_boost': (0, 255, 0),
            'enemy_static': (128, 0, 128),
            'enemy_chasing': (255, 0, 255),
            'enemy_intelligent': (255, 165, 0),
        }
        return color_map.get(name, (255, 255, 255))

    def _create_simple_wall(self, wall_type, theme):
        """Create simple wall sprite"""
        from config import THEMES
        theme_colors = THEMES.get(theme, THEMES['desert'])

        color_key = f'{wall_type}_color'
        color = theme_colors.get(color_key, (128, 128, 128))

        surface = pygame.Surface((40, 40))
        surface.fill(color)
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, 40, 40), 2)
        return surface

    def _create_explosion_frame(self, frame_num):
        """Create simple explosion frame"""
        surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        progress = frame_num / 8
        radius = int(20 * progress)
        alpha = int(255 * (1 - progress))
        color = (255, int(255 * (1 - progress)), 0, alpha)
        pygame.draw.circle(surface, color, (20, 20), radius)
        return surface

    def _create_circle_surface(self, size, color):
        """Create a circular surface"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2)
        return surface

    def _create_star_surface(self, size, color):
        """Create a star-shaped surface for power-ups"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        # Draw a simple star
        center = size // 2
        points = []
        import math

        for i in range(10):
            angle = (i * math.pi / 5) - (math.pi / 2)
            radius = center if i % 2 == 0 else center // 2
            x = center + int(radius * math.cos(angle))
            y = center + int(radius * math.sin(angle))
            points.append((x, y))

        pygame.draw.polygon(surface, color, points)
        return surface

    def get_image(self, name):
        """Get an image by name"""
        return self.images.get(name)

    def get_sound(self, name):
        """Get a sound by name"""
        return self.sounds.get(name)

    def play_sound(self, name, volume=1.0):
        """Play a sound effect"""
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.set_volume(volume)
                sound.play()
            except:
                pass  # Silently fail if sound can't play


# Global instance
_asset_loader = None


def get_asset_loader():
    """Get the global asset loader instance"""
    global _asset_loader
    if _asset_loader is None:
        _asset_loader = AssetLoader()
    return _asset_loader


# Test
if __name__ == "__main__":
    pygame.init()

    print("=" * 60)
    print("🎨 ASSET LOADER TEST")
    print("=" * 60 + "\n")

    # Load assets
    loader = get_asset_loader()

    # Test getting assets
    print("\n--- Testing Asset Access ---")
    bomb_img = loader.get_image('bomb')
    print(f"Bomb image: {bomb_img}")

    explosion_sound = loader.get_sound('explosion')
    print(f"Explosion sound: {explosion_sound}")

    # Test playing sound
    print("\n--- Testing Sound Playback ---")
    loader.play_sound('bomb_place')
    print("Played bomb_place sound")

    pygame.time.wait(200)

    loader.play_sound('explosion')
    print("Played explosion sound")

    print("\n" + "=" * 60)
    print("✅ Asset Loader test completed!")
    print("=" * 60)