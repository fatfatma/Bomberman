# patterns/behavioral/observer.py
"""
Observer Pattern - Game Event System
Allows objects to subscribe to and receive notifications about game events
"""

from abc import ABC, abstractmethod
from enum import Enum


class GameEvent(Enum):
    """
    Enumeration of all possible game events.
    """
    PLAYER_MOVED = "player_moved"
    BOMB_PLACED = "bomb_placed"
    BOMB_EXPLODED = "bomb_exploded"
    WALL_DESTROYED = "wall_destroyed"
    POWERUP_SPAWNED = "powerup_spawned"
    POWERUP_COLLECTED = "powerup_collected"
    PLAYER_DIED = "player_died"
    ENEMY_DIED = "enemy_died"
    GAME_WON = "game_won"
    GAME_LOST = "game_lost"
    SCORE_UPDATED = "score_updated"


class Observer(ABC):
    """
    Abstract observer interface.
    All observers must implement the update method.
    """

    @abstractmethod
    def update(self, event, data):
        """
        Called when an event occurs.

        Args:
            event (GameEvent): The event that occurred
            data (dict): Additional data about the event
        """
        pass


class Subject:
    """
    Subject class that observers can subscribe to.
    Maintains a list of observers and notifies them of events.
    """

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """
        Add an observer to the subscription list.

        Args:
            observer (Observer): Observer to add
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"✅ Observer {observer.__class__.__name__} attached")

    def detach(self, observer):
        """
        Remove an observer from the subscription list.

        Args:
            observer (Observer): Observer to remove
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"❌ Observer {observer.__class__.__name__} detached")

    def notify(self, event, data=None):
        """
        Notify all observers about an event.

        Args:
            event (GameEvent): The event that occurred
            data (dict): Additional data about the event
        """
        for observer in self._observers:
            observer.update(event, data)


class GameEventManager(Subject):
    """
    Singleton event manager for the entire game.
    Centralized event notification system.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameEventManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            super().__init__()
            self._initialized = True
            print("🎮 Game Event Manager initialized")

    def trigger_event(self, event, data=None):
        """
        Trigger a game event.

        Args:
            event (GameEvent): The event to trigger
            data (dict): Additional data about the event
        """
        print(f"📢 Event triggered: {event.value}")
        self.notify(event, data)


# Concrete Observer Examples

class ScoreObserver(Observer):
    """
    Observer that tracks score changes.
    """

    def __init__(self):
        self.score = 0

    def update(self, event, data):
        """Update score based on game events"""
        if event == GameEvent.WALL_DESTROYED:
            self.score += 10
            print(f"  💰 Score: +10 (Wall destroyed) | Total: {self.score}")
        elif event == GameEvent.ENEMY_DIED:
            self.score += 50
            print(f"  💰 Score: +50 (Enemy defeated) | Total: {self.score}")
        elif event == GameEvent.POWERUP_COLLECTED:
            self.score += 25
            print(f"  💰 Score: +25 (Power-up collected) | Total: {self.score}")


class SoundObserver(Observer):
    """
    Observer that plays sounds for game events.
    Uses pygame.mixer for actual sound playback.
    """

    def __init__(self):
        import pygame
        pygame.mixer.init()
        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        """Load sound files or create placeholder sounds"""
        import pygame

        # Try to load sounds from assets folder
        sound_files = {
            'bomb_place': 'assets/sounds/bomb_place.wav',
            'explosion': 'assets/sounds/explosion.wav',
            'powerup': 'assets/sounds/powerup.wav',
            'death': 'assets/sounds/death.wav',
            'wall_break': 'assets/sounds/wall_break.wav'
        }

        for name, path in sound_files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
                print(f"✅ Loaded sound: {name}")
            except:
                # Create a simple beep sound as placeholder
                self.sounds[name] = self._create_placeholder_sound(name)
                print(f"⚠️ Using placeholder for: {name}")

    def _create_placeholder_sound(self, sound_type):
        """Create a simple beep sound as placeholder"""
        import pygame
        import numpy as np

        # Generate a simple beep at different frequencies
        frequency_map = {
            'bomb_place': 440,  # A note
            'explosion': 220,  # Lower A
            'powerup': 880,  # Higher A
            'death': 110,  # Very low A
            'wall_break': 660  # E note
        }

        frequency = frequency_map.get(sound_type, 440)
        sample_rate = 22050
        duration = 0.1  # 100ms

        # Generate sine wave
        samples = int(sample_rate * duration)
        wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, samples))

        # Convert to 16-bit integers
        wave = (wave * 32767).astype(np.int16)

        # Create stereo sound
        stereo_wave = np.column_stack((wave, wave))

        # Create pygame Sound object
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound

    def update(self, event, data):
        """Play appropriate sound for events"""
        sound_map = {
            GameEvent.BOMB_PLACED: 'bomb_place',
            GameEvent.BOMB_EXPLODED: 'explosion',
            GameEvent.POWERUP_COLLECTED: 'powerup',
            GameEvent.PLAYER_DIED: 'death',
            GameEvent.WALL_DESTROYED: 'wall_break'
        }

        sound_name = sound_map.get(event)
        if sound_name and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass  # Silently fail if sound can't play


class NetworkObserver(Observer):
    """
    Observer that sends game events to other players over network.
    """

    def update(self, event, data):
        """Send event data to other players"""
        if event in [GameEvent.PLAYER_MOVED, GameEvent.BOMB_PLACED,
                     GameEvent.BOMB_EXPLODED, GameEvent.PLAYER_DIED]:
            print(f"  🌐 Sending to network: {event.value} - {data}")


class StatisticsObserver(Observer):
    """
    Observer that tracks game statistics.
    """

    def __init__(self):
        self.stats = {
            'bombs_placed': 0,
            'walls_destroyed': 0,
            'powerups_collected': 0,
            'enemies_killed': 0,
            'deaths': 0
        }

    def update(self, event, data):
        """Update statistics based on events"""
        if event == GameEvent.BOMB_PLACED:
            self.stats['bombs_placed'] += 1
        elif event == GameEvent.WALL_DESTROYED:
            self.stats['walls_destroyed'] += 1
        elif event == GameEvent.POWERUP_COLLECTED:
            self.stats['powerups_collected'] += 1
        elif event == GameEvent.ENEMY_DIED:
            self.stats['enemies_killed'] += 1
        elif event == GameEvent.PLAYER_DIED:
            self.stats['deaths'] += 1

    def print_stats(self):
        """Print current statistics"""
        print("\n📊 Game Statistics:")
        for key, value in self.stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")


# Usage Example
if __name__ == "__main__":
    print("=== Testing Observer Pattern ===\n")

    # Create event manager (Singleton)
    event_manager = GameEventManager()

    # Create observers
    score_observer = ScoreObserver()
    sound_observer = SoundObserver()
    network_observer = NetworkObserver()
    stats_observer = StatisticsObserver()

    # Attach observers
    event_manager.attach(score_observer)
    event_manager.attach(sound_observer)
    event_manager.attach(network_observer)
    event_manager.attach(stats_observer)

    # Simulate game events
    print("\n--- Simulating Game Events ---\n")

    event_manager.trigger_event(GameEvent.BOMB_PLACED, {'player': 1, 'position': (5, 5)})
    event_manager.trigger_event(GameEvent.BOMB_EXPLODED, {'position': (5, 5), 'power': 3})
    event_manager.trigger_event(GameEvent.WALL_DESTROYED, {'type': 'breakable', 'position': (6, 5)})
    event_manager.trigger_event(GameEvent.POWERUP_SPAWNED, {'type': 'bomb_count', 'position': (6, 5)})
    event_manager.trigger_event(GameEvent.POWERUP_COLLECTED, {'type': 'bomb_count', 'player': 1})
    event_manager.trigger_event(GameEvent.ENEMY_DIED, {'type': 'chasing', 'position': (7, 5)})

    # Print final statistics
    stats_observer.print_stats()

    print("\n✅ Observer Pattern test completed!")