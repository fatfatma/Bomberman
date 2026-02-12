# controllers/network_controller.py
"""
Network Game Controller
Extends GameController for online multiplayer
"""

from controllers.game_controller import GameController
from network.client import GameClient


class NetworkGameController(GameController):
    """
    Game controller for online multiplayer.
    Extends GameController with network functionality.
    """

    def __init__(self, username, host='localhost', port=5000):
        """
        Initialize network game controller.

        Args:
            username (str): Player username
            host (str): Server host
            port (int): Server port
        """
        self.username = username
        self.client = GameClient()
        self.network_ready = False
        self.my_player_number = None
        self.opponent_player = None

        # Setup client callbacks
        self._setup_client_callbacks()

        # Connect to server
        print(f"\n🌐 Connecting to multiplayer server...")
        if self.client.connect(host, port):
            self.client.join_game(username)
        else:
            raise ConnectionError("Failed to connect to server")

    def _setup_client_callbacks(self):
        """Setup network event callbacks"""
        self.client.on_game_start = self._on_game_start
        self.client.on_opponent_move = self._on_opponent_move
        self.client.on_opponent_bomb = self._on_opponent_bomb
        self.client.on_opponent_died = self._on_opponent_died
        self.client.on_waiting = self._on_waiting

    def _on_game_start(self, data):
        """Called when game starts"""
        self.my_player_number = data['player_number']
        opponent_name = data['opponent']

        # Initialize game
        if self.my_player_number == 1:
            super().__init__(self.username, opponent_name, theme='desert', is_multiplayer=True)
        else:
            super().__init__(opponent_name, self.username, theme='forest', is_multiplayer=True)

        self.network_ready = True
        print(f"✅ Network game initialized!")

    def _on_opponent_move(self, data):
        """Called when opponent moves"""
        if not self.network_ready:
            return

        # Get opponent player
        opponent_num = 2 if self.my_player_number == 1 else 1
        opponent = self.players[opponent_num - 1]

        # Update opponent position
        opponent.grid_x = data['x']
        opponent.grid_y = data['y']
        opponent.x = data['x'] * 40  # TILE_SIZE
        opponent.y = data['y'] * 40
        opponent.rect.x = opponent.x
        opponent.rect.y = opponent.y
        opponent.direction = data['direction']

    def _on_opponent_bomb(self, data):
        """Called when opponent places bomb"""
        if not self.network_ready:
            return

        from models.bomb import Bomb

        opponent_num = 2 if self.my_player_number == 1 else 1
        opponent = self.players[opponent_num - 1]

        # Create bomb
        bomb = Bomb(data['x'], data['y'], data['power'], opponent)
        self.bombs.append(bomb)
        opponent.place_bomb()

    def _on_opponent_died(self, data):
        """Called when opponent dies"""
        if not self.network_ready:
            return

        opponent_num = 2 if self.my_player_number == 1 else 1
        opponent = self.players[opponent_num - 1]
        opponent.die()

        # We won!
        self.game_over = True
        self.winner = self.players[self.my_player_number - 1]

    def _on_waiting(self, data):
        """Called when waiting for opponent"""
        print(f"⏳ {data['message']}")

    def handle_input(self, player_id, dx, dy, place_bomb=False):
        """
        Override to send network updates.
        Only handle input for our player.
        """
        # Only handle our player
        if player_id != self.my_player_number:
            return

        # Call parent method
        super().handle_input(player_id, dx, dy, place_bomb)

        # Send to network
        if not self.network_ready:
            return

        player = self.players[player_id - 1]

        # Send movement
        if dx != 0 or dy != 0:
            self.client.send_player_move(player.grid_x, player.grid_y, player.direction)

        # Send bomb placement
        if place_bomb and player.bombs_placed > 0:
            # Find the bomb we just placed
            for bomb in self.bombs:
                if bomb.owner == player and bomb.timer == 3000:  # Just placed
                    self.client.send_bomb_placed(bomb.grid_x, bomb.grid_y, bomb.power)
                    break

    def update(self, dt):
        """Override to handle network state"""
        if not self.network_ready:
            return

        # Call parent update
        super().update(dt)

        # Check if we died
        my_player = self.players[self.my_player_number - 1]
        if not my_player.state_manager.is_alive() and not self.game_over:
            self.client.send_player_died()

    def disconnect(self):
        """Disconnect from server"""
        if self.client.connected:
            self.client.disconnect()