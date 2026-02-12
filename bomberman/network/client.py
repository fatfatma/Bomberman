# network/client.py
"""
Game Client for Online Multiplayer
Uses Facade Pattern for simplified network operations
"""

from patterns.structural.facade import NetworkFacade
from config import SERVER_HOST, SERVER_PORT


class GameClient:
    """
    Game client for online multiplayer.
    """

    def __init__(self):
        """Initialize game client"""
        self.facade = NetworkFacade()
        self.connected = False
        self.player_number = None
        self.game_id = None
        self.opponent_name = None

        # Callbacks
        self.on_game_start = None
        self.on_opponent_move = None
        self.on_opponent_bomb = None
        self.on_opponent_died = None
        self.on_waiting = None

        # Register handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register message handlers"""
        self.facade.register_handler('game_start', self._handle_game_start)
        self.facade.register_handler('opponent_move', self._handle_opponent_move)
        self.facade.register_handler('opponent_bomb', self._handle_opponent_bomb)
        self.facade.register_handler('opponent_died', self._handle_opponent_died)
        self.facade.register_handler('waiting', self._handle_waiting)

    def connect(self, host=SERVER_HOST, port=SERVER_PORT):
        """
        Connect to server.

        Args:
            host (str): Server host
            port (int): Server port

        Returns:
            bool: True if connected
        """
        print(f"🔌 Connecting to server {host}:{port}...")
        self.connected = self.facade.connect(host, port)
        return self.connected

    def disconnect(self):
        """Disconnect from server"""
        if self.connected:
            self.facade.send_message('disconnect', {})
            self.facade.disconnect()
            self.connected = False

    def join_game(self, username):
        """
        Request to join a game.

        Args:
            username (str): Player username
        """
        print(f"📤 Requesting to join game as '{username}'...")
        return self.facade.send_join_game(username)

    def send_player_move(self, x, y, direction):
        """Send player movement to server"""
        if not self.connected or not self.player_number:
            return False

        return self.facade.send_player_move(self.player_number, x, y, direction)

    def send_bomb_placed(self, x, y, power):
        """Send bomb placement to server"""
        if not self.connected or not self.player_number:
            return False

        return self.facade.send_bomb_placed(self.player_number, x, y, power)

    def send_player_died(self):
        """Send player death to server"""
        if not self.connected or not self.player_number:
            return False

        return self.facade.send_player_died(self.player_number)

    # Message Handlers

    def _handle_game_start(self, data):
        """Handle game start message"""
        self.game_id = data.get('game_id')
        self.player_number = data.get('player_number')
        self.opponent_name = data.get('opponent')

        print(f"\n🎮 Game {self.game_id} started!")
        print(f"   You are Player {self.player_number}")
        print(f"   Opponent: {self.opponent_name}\n")

        if self.on_game_start:
            self.on_game_start(data)

    def _handle_opponent_move(self, data):
        """Handle opponent movement"""
        if self.on_opponent_move:
            self.on_opponent_move(data)

    def _handle_opponent_bomb(self, data):
        """Handle opponent bomb placement"""
        if self.on_opponent_bomb:
            self.on_opponent_bomb(data)

    def _handle_opponent_died(self, data):
        """Handle opponent death"""
        print(f"\n💀 Opponent died! You win!")

        if self.on_opponent_died:
            self.on_opponent_died(data)

    def _handle_waiting(self, data):
        """Handle waiting message"""
        message = data.get('message', 'Waiting...')
        print(f"⏳ {message}")

        if self.on_waiting:
            self.on_waiting(data)


# Test client
if __name__ == "__main__":
    import time

    print("=" * 60)
    print("🎮 BOMBERMAN GAME CLIENT TEST")
    print("=" * 60)

    client = GameClient()

    if client.connect():
        # Request to join game
        username = input("\nEnter your username: ")
        client.join_game(username)

        print("\nConnected! Waiting for game to start...")
        print("Press Ctrl+C to disconnect\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️  Disconnecting...")
            client.disconnect()
            print("👋 Disconnected")
    else:
        print("❌ Failed to connect to server")
        print("   Make sure the server is running!")