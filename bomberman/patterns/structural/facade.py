# patterns/structural/facade.py
"""
Facade Pattern - Network Facade
Provides a simplified interface for complex network operations
"""

import socket
import json
import threading


class NetworkFacade:
    """
    Facade that simplifies network operations.
    Hides the complexity of socket programming, threading, and message handling.
    """

    def __init__(self):
        self.socket = None
        self.connected = False
        self.receive_thread = None
        self.message_handlers = {}
        self.running = False

    def connect(self, host, port):
        """
        Connect to server with simplified interface.

        Args:
            host (str): Server host
            port (int): Server port

        Returns:
            bool: True if connected successfully
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            self.running = True

            # Start receiving messages in background
            self.receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
            self.receive_thread.start()

            print(f"✅ Connected to server: {host}:{port}")
            return True

        except Exception as e:
            print(f"❌ Connection failed: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Disconnect from server"""
        self.running = False
        self.connected = False

        if self.socket:
            try:
                self.socket.close()
                print("🔒 Disconnected from server")
            except:
                pass

    def send_message(self, message_type, data):
        """
        Send a message to server with simplified interface.

        Args:
            message_type (str): Type of message
            data (dict): Message data

        Returns:
            bool: True if sent successfully
        """
        if not self.connected:
            print("❌ Not connected to server")
            return False

        try:
            message = {
                'type': message_type,
                'data': data
            }

            json_message = json.dumps(message)
            self.socket.sendall(json_message.encode() + b'\n')
            return True

        except Exception as e:
            print(f"❌ Send failed: {e}")
            self.connected = False
            return False

    def register_handler(self, message_type, handler):
        """
        Register a handler for specific message type.

        Args:
            message_type (str): Type of message to handle
            handler (callable): Function to call when message received
        """
        self.message_handlers[message_type] = handler
        print(f"✅ Handler registered for: {message_type}")

    def _receive_messages(self):
        """Background thread that receives messages"""
        buffer = ""

        while self.running and self.connected:
            try:
                data = self.socket.recv(4096).decode()
                if not data:
                    print("⚠️ Server closed connection")
                    self.connected = False
                    break

                buffer += data

                # Process complete messages (separated by newlines)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self._process_message(line)

            except Exception as e:
                if self.running:
                    print(f"❌ Receive error: {e}")
                    self.connected = False
                break

    def _process_message(self, message_str):
        """Process received message"""
        try:
            message = json.loads(message_str)
            message_type = message.get('type')
            data = message.get('data', {})

            # Call registered handler if exists
            if message_type in self.message_handlers:
                self.message_handlers[message_type](data)
            else:
                print(f"⚠️ No handler for message type: {message_type}")

        except Exception as e:
            print(f"❌ Message processing error: {e}")

    # High-level game-specific methods

    def send_player_move(self, player_id, x, y, direction):
        """Send player movement"""
        return self.send_message('player_move', {
            'player_id': player_id,
            'x': x,
            'y': y,
            'direction': direction
        })

    def send_bomb_placed(self, player_id, x, y, power):
        """Send bomb placement"""
        return self.send_message('bomb_placed', {
            'player_id': player_id,
            'x': x,
            'y': y,
            'power': power
        })

    def send_player_died(self, player_id):
        """Send player death"""
        return self.send_message('player_died', {
            'player_id': player_id
        })

    def send_join_game(self, username):
        """Send join game request"""
        return self.send_message('join_game', {
            'username': username
        })

    def send_game_ready(self):
        """Send game ready signal"""
        return self.send_message('game_ready', {})


class ServerFacade:
    """
    Facade for server-side network operations.
    Simplifies server socket handling and client management.
    """

    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}  # client_id -> (socket, address)
        self.running = False
        self.accept_thread = None
        self.message_handlers = {}

    def start(self):
        """Start the server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True

            print(f"✅ Server started on {self.host}:{self.port}")

            # Start accepting connections
            self.accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
            self.accept_thread.start()

            return True

        except Exception as e:
            print(f"❌ Server start failed: {e}")
            return False

    def stop(self):
        """Stop the server"""
        self.running = False

        # Close all client connections
        for client_id, (client_socket, _) in list(self.clients.items()):
            try:
                client_socket.close()
            except:
                pass

        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

        print("🔒 Server stopped")

    def _accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                client_id = len(self.clients) + 1
                self.clients[client_id] = (client_socket, address)

                print(f"✅ Client {client_id} connected from {address}")

                # Start thread to handle this client
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_id, client_socket),
                    daemon=True
                )
                client_thread.start()

            except:
                if self.running:
                    print("❌ Accept connection error")
                break

    def _handle_client(self, client_id, client_socket):
        """Handle messages from a client"""
        buffer = ""

        while self.running:
            try:
                data = client_socket.recv(4096).decode()
                if not data:
                    break

                buffer += data

                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self._process_client_message(client_id, line)

            except Exception as e:
                print(f"❌ Client {client_id} error: {e}")
                break

        # Client disconnected
        self._remove_client(client_id)

    def _process_client_message(self, client_id, message_str):
        """Process message from client"""
        try:
            message = json.loads(message_str)
            message_type = message.get('type')
            data = message.get('data', {})
            data['client_id'] = client_id  # Add client ID

            # Call registered handler
            if message_type in self.message_handlers:
                self.message_handlers[message_type](data)

        except Exception as e:
            print(f"❌ Message processing error: {e}")

    def _remove_client(self, client_id):
        """Remove disconnected client"""
        if client_id in self.clients:
            try:
                self.clients[client_id][0].close()
            except:
                pass
            del self.clients[client_id]
            print(f"⚠️ Client {client_id} disconnected")

    def register_handler(self, message_type, handler):
        """Register message handler"""
        self.message_handlers[message_type] = handler
        print(f"✅ Server handler registered for: {message_type}")

    def broadcast(self, message_type, data, exclude_client=None):
        """
        Broadcast message to all clients.

        Args:
            message_type (str): Message type
            data (dict): Message data
            exclude_client (int): Client ID to exclude (optional)
        """
        message = {
            'type': message_type,
            'data': data
        }
        json_message = json.dumps(message).encode() + b'\n'

        for client_id, (client_socket, _) in list(self.clients.items()):
            if exclude_client and client_id == exclude_client:
                continue

            try:
                client_socket.sendall(json_message)
            except:
                self._remove_client(client_id)

    def send_to_client(self, client_id, message_type, data):
        """Send message to specific client"""
        if client_id not in self.clients:
            return False

        message = {
            'type': message_type,
            'data': data
        }
        json_message = json.dumps(message).encode() + b'\n'

        try:
            self.clients[client_id][0].sendall(json_message)
            return True
        except:
            self._remove_client(client_id)
            return False


# Usage Example
if __name__ == "__main__":
    print("=== Testing Facade Pattern ===\n")

    print("Facade Pattern simplifies complex network operations:")
    print("  ✓ Hides socket programming complexity")
    print("  ✓ Provides simple send/receive interface")
    print("  ✓ Manages threading automatically")
    print("  ✓ Handles JSON serialization")
    print("  ✓ Provides high-level game-specific methods")

    print("\n✅ Facade Pattern implemented!")