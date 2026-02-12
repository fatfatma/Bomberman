# 🎮 Bomberman Game - Design Patterns Project

A fully-featured online multiplayer Bomberman game implementing **9 design patterns** as part of the Design Patterns course project.

## 👥 Team Members
- **Fatma Yıldız** - 220401086
- **Dilan Elif Başboğa** - 220401033
- **Class:** Computer Engineering, 3rd Year
- **Course:** Design Patterns (2025)
- **Instructor:** Prof. Dr. Doğan Aydın
- **University:** İzmir Katip Çelebi University

---

## 📋 Table of Contents
1. [Quick Start](#-quick-start)
2. [Project Overview](#-project-overview)
3. [Design Patterns](#-design-patterns-implemented-9)
4. [Technologies](#-technologies)
5. [Installation](#-installation--setup)
6. [How to Play](#-how-to-play)
7. [Game Features](#-features)
8. [Project Structure](#-project-structure)
9. [Database & Deployment](#-database--deployment)
10. [Bonus Features](#-bonus-features)

---

## 🚀 Quick Start

### Local Play (Single/Multiplayer)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r bomberman/requirements.txt
python bomberman/main.py
```

### Online Multiplayer
```

### Online Multiplayer

**Terminal 1 - Server:**
```bash
python bomberman/network/server.py
# Server starts on 0.0.0.0:5000
```

**Terminal 2 & 3 - Clients:**
```bash
python bomberman/main.py
# Menu → Online Multiplayer → Join Server
```

**Note:** MySQL optional (needed only for leaderboard). Gameplay works offline.

---

## 🎯 Project Overview

Modern Bomberman implementation demonstrating real-world application of **9 design patterns**. Supports local/online multiplayer, intelligent AI enemies with pathfinding, and complete user management system.

### Key Highlights
✅ **9 Design Patterns** fully integrated  
✅ **Online Multiplayer** with lobby system (+5 bonus)  
✅ **A* Pathfinding** for intelligent AI (+5 bonus)  
✅ **Professional UI/UX** with animations (+5 bonus)  
✅ **Database Integration** for users & leaderboards  
✅ **Docker Deployment** ready  

---

## 🎨 Design Patterns Implemented (9)

### 1️⃣ Singleton Pattern ✅
**Location:** `database/repository.py`

Ensures only one database connection exists throughout the application.

```python
class Database(Singleton):
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
```

**Usage:** All repositories share the same DB connection instance.

---

### 2️⃣ Factory Method Pattern ✅
**Location:** `patterns/creational/factory.py`

Creates game objects without exposing creation logic.

**Factories:**
- `WallFactory`: Creates Unbreakable/Breakable/Hard walls
- `PowerUpFactory`: Creates different power-up types
- `EnemyFactory`: Creates AI strategies

```python
wall = WallFactory.create_wall('breakable', x, y, theme='desert')
powerup = PowerUpFactory.create_powerup('bomb_count', x, y)
```

---

### 3️⃣ Decorator Pattern ✅
**Location:** `patterns/structural/decorator.py` & `models/powerup.py`

Dynamically adds abilities to players via power-ups.

**Decorators:**
- `SpeedBoostDecorator`: +2 speed
- `WallPassDecorator`: Walk through walls

```python
class SpeedPowerUp(PowerUp):
    def apply(self, player):
        decorated = SpeedBoostDecorator(player)
        player.speed = decorated.get_speed()  # +2
```

---

### 4️⃣ Observer Pattern ✅
**Location:** `patterns/behavioral/observer.py`

Notifies multiple observers when game events occur.

**Event Manager** triggers:
- `powerup_collected` → ScoreObserver (+25 points)
- `bomb_placed` → SoundObserver (plays sound)
- `bomb_exploded` → Multiple observers
- `enemy_died` → StatisticsObserver

```python
event_manager.notify({
    'type': 'powerup_collected',
    'player_id': 1,
    'points': 25
})
```

---

### 5️⃣ Strategy Pattern ✅
**Location:** `patterns/behavioral/strategy.py`

Enables different AI behaviors swapped at runtime.

**Strategies:**
- `StaticAIStrategy`: Random movement
- `ChasingAIStrategy`: Follows nearest player
- `IntelligentAIStrategy`: A* pathfinding (BONUS +5)

```python
class Enemy:
    def __init__(self, strategy: AIStrategy):
        self.strategy = strategy
    
    def update(self):
        dx, dy = self.strategy.calculate_move(self, walls, players, enemies)
        self.move(dx, dy)
```

---

### 6️⃣ State Pattern ✅
**Location:** `patterns/behavioral/state.py` & `models/player.py`

Manages player lifecycle with different behaviors per state.

**Player States:**
- `NormalState`: Default state
- `InvincibleState`: Immune to damage (golden glow)
- `StunnedState`: Cannot move (red border)
- `DeadState`: Game over for player

```python
class PlayerStateManager:
    def apply_invincibility(self, duration=5000):
        self.change_state(InvincibleState(self.player, duration))
    
    def stun(self, duration=2000):
        self.change_state(StunnedState(self.player, duration))
    
    def die(self):
        self.change_state(DeadState(self.player))
    
    def is_alive(self) -> bool:
        return not isinstance(self.current_state, DeadState)
```

---

### 7️⃣ Repository Pattern ✅
**Location:** `database/repository.py`, `database/user_repository.py`, `database/game_repository.py`

Abstracts database operations with clean data access layer.

**Repositories:**
- `UserRepository`: User CRUD, authentication
- `GameRepository`: Game stats, leaderboard, preferences

```python
class Repository(ABC):
    def create(self, entity: Dict) -> bool
    def read(self, entity_id: int) -> Dict
    def update(self, entity: Dict) -> bool
    def delete(self, entity_id: int) -> bool
    def read_all(self) -> List[Dict]
```

---

### 8️⃣ Facade Pattern ✅
**Location:** `patterns/structural/facade.py` & `network/server.py`

Simplifies complex network operations.

```python
class ServerFacade:
    def __init__(self, host: str, port: int):
        self.socket = socket.socket()        # Hidden
        self.thread = threading.Thread()     # Hidden
        self.handlers = {}                   # Hidden
    
    def start(self) -> bool
    def register_handler(msg_type: str, callback)
    def send_message(client, data: Dict)
    def receive_message(client) -> Dict
```

---

### 9️⃣ MVC Pattern ✅
**Location:** `models/`, `views/`, `controllers/`

Separates concerns into Model-View-Controller architecture.

**Components:**
- **Models:** Player, Bomb, Wall, Enemy, PowerUp
- **Views:** GameView, MenuView, LeaderboardView
- **Controllers:** GameController, NetworkGameController

```
User Input
    ↓
Controller.handle_input()
    ↓
Model.update() + Model.check_collisions()
    ↓
View.render(game_state)
    ↓
Display on Screen
```

---

## 💻 Technologies

| Tech | Version | Purpose |
|------|---------|---------|
| **Python** | 3.12+ | Core language |
| **Pygame** | 2.5.2 | Game engine |
| **MySQL** | 8.0 | Database (optional) |
| **Docker** | Latest | Containerization |
| **Socket** | Native | Network communication |
| **Threading** | Native | Async operations |

---

## 📦 Installation & Setup

### 1. Clone Repository
```bash
cd bomberman_project
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux/Mac
# or
.venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r bomberman/requirements.txt
```

### 4. Optional: Setup MySQL Database
```bash
mysql -u root -p < bomberman/db_init.sql
```

Edit `bomberman/config.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'bomberman_db'
}
```

### 5. Run the Game
```bash
python bomberman/main.py
```

---

## 🎮 How to Play

### Controls
| Action | Player 1 | Player 2 |
|--------|----------|----------|
| Move | W/A/S/D | Arrow Keys |
| Bomb | SPACE | ENTER |
| Pause | ESC | ESC |
| Restart | R | R |

### Game Modes
1. **Single Player** - Play against 3 AI enemies
2. **Local Multiplayer** - 2 players on same keyboard
3. **Online Multiplayer** - Play against another player

### Objective
- 💣 Destroy breakable walls with bombs
- 🎁 Collect power-ups to enhance abilities
- 👾 Eliminate AI enemies or defeat other player
- 🏆 Get highest score and reach leaderboard

---

## ✨ Features

### Gameplay
- ✅ Classic Bomberman mechanics
- ✅ 4-directional bomb explosions
- ✅ Multiple wall types (Unbreakable/Breakable/Hard)
- ✅ 5 different power-up types
- ✅ 3 AI difficulty levels

### Map System
**Wall Types:**
- **Unbreakable:** Permanent obstacles
- **Breakable:** Destroyed in 1 hit
- **Hard:** Requires 3 hits

**Themes:**
- Desert (sand & stone)
- Forest (green & nature)
- City (urban elements)

### Power-Ups
- 💣 Bomb Count (+1)
- 💥 Bomb Power (+1 radius)
- ⚡ Speed Boost (+2 speed)
- 🛹 Skateboard (+3 speed = max)
- 🚪 Wall Pass (walk through walls)

### AI System
- 🟢 **Static AI:** Random movement
- 🟡 **Chasing AI:** Follows nearest player
- 🔴 **Intelligent AI:** A* pathfinding

### Database Features
- ✅ User registration & authentication
- ✅ Game statistics (wins/losses/total games)
- ✅ Leaderboard (top 10 scores)
- ✅ User preferences (theme selection)

---

## 📁 Project Structure

```
bomberman/
├── main.py                   # Game entry point
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
│
├── models/                   # Game entities
│   ├── player.py            # Player with states
│   ├── bomb.py              # Bombs & explosions
│   ├── wall.py              # Wall types
│   ├── powerup.py           # Power-ups with decorators
│   └── enemy.py             # Enemies with AI
│
├── views/                    # Rendering layer
│   ├── game_view.py         # Game screen
│   ├── menu_view.py         # Menus
│   └── leaderboard_view.py  # Leaderboard
│
├── controllers/              # Logic layer
│   ├── game_controller.py   # Game logic
│   └── network_controller.py # Network logic
│
├── patterns/                 # Design patterns
│   ├── creational/
│   │   ├── factory.py       # Factory Method
│   │   └── singleton.py     # Singleton
│   ├── structural/
│   │   ├── decorator.py     # Decorator
│   │   └── facade.py        # Facade
│   └── behavioral/
│       ├── strategy.py      # Strategy
│       ├── observer.py      # Observer
│       └── state.py         # State
│
├── database/                 # Data layer
│   ├── repository.py        # Base Repository
│   ├── user_repository.py   # User CRUD
│   └── game_repository.py   # Game stats CRUD
│
├── network/                  # Networking
│   ├── server.py            # Game server
│   └── client.py            # Network client
│
└── test/                     # Tests
    ├── test_models.py
    ├── test_enemies.py
    ├── test_powerups.py
    └── test_repository.py
```

---

## 💾 Database & Deployment

### Database Schema

**users table:** Player accounts (username, password_hash)  
**game_stats table:** Statistics (wins, losses, total_games)  
**leaderboard table:** Score tracking  
**user_preferences table:** Theme & settings  

### Docker Deployment

**MySQL Container:**
- Image: mysql:8.0
- Port: 3307 → 3306
- Database: bomberman_db
- Persistent: mysql_data volume

**Game Server Container:**
- Base: Python 3.12
- Port: 5000
- DB: db:3306 (Docker network)

**Start:**
```bash
docker-compose up -d
```

All dependencies containerized. Single command deployment with persistent data.

---

## 🏆 Bonus Features

### 1. A* Pathfinding Algorithm (+5 points)
Intelligent enemy AI using A* algorithm to find shortest path to player.
- Location: `patterns/behavioral/strategy.py`
- Heuristic-based pathfinding
- Dynamic recalculation
- Obstacle avoidance

### 2. Professional UI/UX (+5 points)
- Animated menus with transitions
- Visual feedback on all actions
- Particle effects on explosions
- Health bars for hard walls
- Floating power-ups
- Player state indicators (glow, stun, death)

### 3. Multiplayer Lobby System (+5 points)
- Automatic player matching
- Waiting room system
- Real-time synchronization
- Connection management
- Graceful disconnect handling

---

## 🧪 Testing

**Pattern Tests:**
```bash
python bomberman/patterns/creational/singleton.py
python bomberman/patterns/creational/factory.py
python bomberman/patterns/behavioral/observer.py
python bomberman/patterns/behavioral/strategy.py
```

**Repository Test (requires MySQL):**
```bash
python bomberman/test/test_repository.py
```

**Network Test:**
```bash
# Terminal 1: Server
python bomberman/network/server.py

# Terminal 2: Client
python bomberman/network/client.py
```

---

## 📚 References

1. Freeman & Robson. *Head First Design Patterns*. O'Reilly Media, 2004.
2. Gamma, Helm, Johnson, Vlissides. *Design Patterns: Elements of Reusable Object-Oriented Software*. 1995.
3. Robert Nystrom. *Game Programming Patterns*. https://gameprogrammingpatterns.com/
4. Refactoring.Guru. *Design Patterns*. https://refactoring.guru/
5. SourceMaking. *Design Patterns*. https://sourcemaking.com/design_patterns

---

## 📝 License

Educational project for İzmir Katip Çelebi University Design Patterns course (2025).

---

## 👏 Acknowledgments

- Prof. Dr. Doğan Aydın for course guidance
- İzmir Katip Çelebi University
- Pygame community
- Design pattern resources

---

**Last Updated:** December 24, 2025  
**Status:** ✅ Complete & Tested
>>>>>>> 230f922 (İlk commit: Proje dosyaları eklendi)
