# network/server.py
"""
Game Server for Online Multiplayer
Uses Facade Pattern for simplified network operations
"""

from patterns.structural.facade import ServerFacade
from config import SERVER_HOST, SERVER_PORT


class GameServer:
    """
    Game server that manages multiplayer sessions.
    """

    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        """Initialize game server"""
        self.facade = ServerFacade(host, port)
        self.games = {}  # game_id -> game_data
        self.clients = {}  # client_id -> player_data
        self.waiting_players = []

        # Register message handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register handlers for different message types"""
        self.facade.register_handler('join_game', self._handle_join_game)
        self.facade.register_handler('player_move', self._handle_player_move)
        self.facade.register_handler('bomb_placed', self._handle_bomb_placed)
        self.facade.register_handler('player_died', self._handle_player_died)
        self.facade.register_handler('disconnect', self._handle_disconnect)

    def start(self):
        """Start the server"""
        print("=" * 60)
        print("🎮 BOMBERMAN GAME SERVER")
        print("=" * 60)

        if self.facade.start():
            print(f"\n✅ Server is running!")
            print(f"   Waiting for players to connect...")
            print(f"   Press Ctrl+C to stop\n")
            print("=" * 60)
            return True
        return False

    def _handle_join_game(self, data):
        """Handle player joining game"""
        client_id = data.get('client_id')
        username = data.get('username')

        print(f"📥 Player '{username}' requesting to join (Client {client_id})")

        # Add to waiting players
        self.waiting_players.append({
            'client_id': client_id,
            'username': username
        })

        self.clients[client_id] = {
            'username': username,
            'player_number': None,
            'game_id': None
        }

        # If 2 players waiting, start game
        if len(self.waiting_players) >= 2:
            self._start_game()
        else:
            # Tell player to wait
            self.facade.send_to_client(client_id, 'waiting', {
                'message': 'Waiting for opponent...'
            })
            print(f"   ⏳ {username} is waiting for opponent...")

    def _start_game(self):
        """Start a new game with 2 players"""
        player1 = self.waiting_players.pop(0)
        player2 = self.waiting_players.pop(0)

        game_id = len(self.games) + 1

        print(f"\n🎮 Starting Game {game_id}:")
        print(f"   Player 1: {player1['username']} (Client {player1['client_id']})")
        print(f"   Player 2: {player2['username']} (Client {player2['client_id']})")

        # Setup game data
        self.games[game_id] = {
            'players': [player1, player2],
            'started': True
        }

        # Update client data
        self.clients[player1['client_id']]['player_number'] = 1
        self.clients[player1['client_id']]['game_id'] = game_id
        self.clients[player2['client_id']]['player_number'] = 2
        self.clients[player2['client_id']]['game_id'] = game_id

        # Send game start to both players
        self.facade.send_to_client(player1['client_id'], 'game_start', {
            'game_id': game_id,
            'player_number': 1,
            'opponent': player2['username']
        })

        self.facade.send_to_client(player2['client_id'], 'game_start', {
            'game_id': game_id,
            'player_number': 2,
            'opponent': player1['username']
        })

        print(f"   ✅ Game {game_id} started!\n")

    def _handle_player_move(self, data):
        """Handle player movement and broadcast to opponent"""
        client_id = data.get('client_id')

        if client_id not in self.clients:
            return

        game_id = self.clients[client_id]['game_id']
        if not game_id or game_id not in self.games:
            return

        # Broadcast to other player in the game
        game = self.games[game_id]
        for player in game['players']:
            if player['client_id'] != client_id:
                self.facade.send_to_client(player['client_id'], 'opponent_move', data)

    def _handle_bomb_placed(self, data):
        """Handle bomb placement and broadcast"""
        client_id = data.get('client_id')

        if client_id not in self.clients:
            return

        game_id = self.clients[client_id]['game_id']
        if not game_id or game_id not in self.games:
            return

        # Broadcast to other player
        game = self.games[game_id]
        for player in game['players']:
            if player['client_id'] != client_id:
                self.facade.send_to_client(player['client_id'], 'opponent_bomb', data)

    def _handle_player_died(self, data):
        """Handle player death and broadcast"""
        client_id = data.get('client_id')

        if client_id not in self.clients:
            return

        game_id = self.clients[client_id]['game_id']
        if not game_id or game_id not in self.games:
            return

        player_number = self.clients[client_id]['player_number']

        print(f"💀 Player {player_number} died in Game {game_id}")

        # Broadcast to other player
        game = self.games[game_id]
        for player in game['players']:
            if player['client_id'] != client_id:
                self.facade.send_to_client(player['client_id'], 'opponent_died', {
                    'player_number': player_number
                })

        # End game
        self._end_game(game_id)

    def _handle_disconnect(self, data):
        """Handle player disconnection"""
        client_id = data.get('client_id')

        if client_id in self.clients:
            username = self.clients[client_id]['username']
            game_id = self.clients[client_id]['game_id']

            print(f"⚠️ Player '{username}' disconnected (Client {client_id})")

            # Remove from waiting list
            self.waiting_players = [p for p in self.waiting_players if p['client_id'] != client_id]

            # End game if in progress
            if game_id and game_id in self.games:
                self._end_game(game_id)

            del self.clients[client_id]

    def _end_game(self, game_id):
        """End a game"""
        if game_id in self.games:
            print(f"🏁 Game {game_id} ended\n")
            del self.games[game_id]

    def stop(self):
        """Stop the server"""
        self.facade.stop()


def main():
    """Run the server"""
    server = GameServer()

    if server.start():
        try:
            # Keep server running
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️  Shutting down server...")
            server.stop()
            print("👋 Server stopped")


if __name__ == "__main__":
    main()