# 🎮 Bomberman Game - Design Patterns Project

A fully-featured online multiplayer Bomberman game implementing 9 design patterns as part of the Design Patterns course project.

## 👥 Team Members
- **Student Names**: Fatma Yıldız 220401086 
- **Student Names**: Dilan Elif Başboğa 220401033
- Computer Engineering Students 3th class. 
- **Course**: Design Patterns 2025
- **Instructor**: Prof. Dr. Doğan Aydın
- **University**: İzmir Katip Çelebi University

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Design Patterns Implemented](#design-patterns-implemented)
3. [Technologies Used](#technologies-used)
4. [Installation & Setup](#installation--setup)
5. [How to Play](#how-to-play)
6. [Features](#features)
7. [Project Structure](#project-structure)
8. [Database Schema](#database-schema)
9. [Bonus Features](#bonus-features)

---

## 🎯 Project Overview

This project is a modern implementation of the classic Bomberman game, designed to demonstrate practical applications of software design patterns. The game supports both local and online multiplayer modes, features AI opponents with different difficulty levels, and includes a complete user management system with statistics tracking.

### Key Highlights
- **9 Design Patterns** fully implemented and integrated
- **Online Multiplayer** with lobby system (+5 bonus)
- **A* Pathfinding** for intelligent AI enemies (+5 bonus)
- **Professional UI/UX** with animations (+5 bonus)
- **Complete Database Integration** for user management and leaderboards
- **MVC Architecture** for clean code organization

---

## 🎨 Design Patterns Implemented

### 1. Singleton Pattern ✅
**Location:** `patterns/creational/singleton.py`

**Purpose:** Ensures only one database connection exists throughout the application.

**Implementation:**
```python
class DatabaseConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
```

**Usage:** Provides a single, shared database connection for all repositories, preventing connection overhead and ensuring data consistency.

---

### 2. Factory Method Pattern ✅
**Location:** `patterns/creational/factory.py`

**Purpose:** Creates different types of game objects without exposing creation logic.

**Implementation:**
- `WallFactory`: Creates Unbreakable, Breakable, and Hard walls
- `PowerUpFactory`: Creates different power-up types
- `create_ai_strategy()`: Creates different AI strategies

**Example:**
```python
wall = WallFactory.create_wall('breakable', x, y, theme='desert')
powerup = PowerUpFactory.create_powerup('bomb_count', x, y)
```

**Benefits:** Decouples object creation from usage, makes it easy to add new types.

---

### 3. Decorator Pattern ✅
**Location:** `patterns/structural/decorator.py`

**Purpose:** Dynamically adds abilities to players without modifying the base Player class.

**Implementation:**
```python
class SpeedBoostDecorator(PlayerDecorator):
    def get_speed(self):
        return self._player_component.get_speed() + self.boost_amount
```

**Usage:** Stack multiple power-ups on a player (speed + bomb count + bomb power).

---

### 4. Facade Pattern ✅
**Location:** `patterns/structural/facade.py`

**Purpose:** Provides a simplified interface for complex network operations.

**Implementation:**
- `NetworkFacade`: Simplifies client-side networking
- `ServerFacade`: Simplifies server-side networking

**Benefits:** Hides socket programming complexity, JSON serialization, and threading.

---

### 5. Strategy Pattern ✅
**Location:** `patterns/behavioral/strategy.py`

**Purpose:** Enables different AI behaviors to be swapped at runtime.

**Implementation:**
- `StaticAIStrategy`: Random movement
- `ChasingAIStrategy`: Follows nearest player
- `IntelligentAIStrategy`: Uses A* pathfinding (Bonus +5)

**Example:**
```python
enemy.set_strategy(create_ai_strategy('intelligent'))
```

---

### 6. Observer Pattern ✅
**Location:** `patterns/behavioral/observer.py`

**Purpose:** Notifies multiple observers when game events occur.

**Implementation:**
```python
event_manager.trigger_event(GameEvent.BOMB_EXPLODED, data)
# ScoreObserver updates score
# SoundObserver plays sound
# NetworkObserver sends to other players
```

**Observers:**
- ScoreObserver: Tracks score
- StatisticsObserver: Tracks game stats
- SoundObserver: Plays sounds (placeholder)
- NetworkObserver: Syncs multiplayer

---

### 7. State Pattern ✅
**Location:** `patterns/behavioral/state.py`

**Purpose:** Manages different player states with different behaviors.

**States:**
- `NormalState`: Default state
- `InvincibleState`: Cannot take damage (flashing effect)
- `StunnedState`: Cannot move (stars around player)
- `DeadState`: Player died (explosion animation)

**Benefits:** Clean state transitions, state-specific rendering and behavior.

---

### 8. Repository Pattern ✅
**Location:** `database/repository.py`, `database/user_repository.py`, `database/game_repository.py`

**Purpose:** Abstracts database operations and provides a clean data access layer.

**Repositories:**
- `UserRepository`: User CRUD, authentication, registration
- `GameRepository`: Game stats, leaderboard, preferences

**Example:**
```python
user = user_repo.authenticate(username, password)
game_repo.update_stats(user_id, won=True)
leaderboard = game_repo.get_leaderboard(10)
```

---

### 9. MVC Pattern ✅
**Location:** `models/`, `views/`, `controllers/`

**Purpose:** Separates concerns into Model-View-Controller architecture.

**Components:**
- **Models:** `Player`, `Bomb`, `Wall`, `Enemy`, `PowerUp`
- **Views:** `GameView`, `MenuView`, `LeaderboardView`
- **Controllers:** `GameController`, `NetworkGameController`

**Benefits:** Clean separation of game logic, rendering, and user input handling.

---

## 💻 Technologies Used

- **Language:** Python 3.12
- **Game Framework:** Pygame 2.5.2
- **Database:** MySQL 8.0
- **Database Driver:** mysql-connector-python 8.2.0
- **Network:** Native Python sockets with JSON messaging
- **IDE:** PyCharm

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd bomberman
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup MySQL Database
```sql
CREATE DATABASE bomberman_db;
USE bomberman_db;

-- Run the SQL schema from the database section below
```

### 4. Configure Database Connection
Edit `config.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password_here',
    'database': 'bomberman_db'
}
```

### 5. Run the Game

**Single Player / Local Multiplayer:**
```bash
python main.py
```

**Online Multiplayer:**

Terminal 1 (Server):
```bash
python network/server.py
```

Terminal 2 & 3 (Clients):
```bash
python main.py
# Select "Online Multiplayer"
```

---

## 🎮 How to Play

### Game Modes
1. **Single Player vs AI** - Play against 3 AI enemies
2. **Local Multiplayer** - 2 players on same keyboard
3. **Online Multiplayer** - Play against another player online

### Controls

**Player 1:**
- `W/A/S/D` - Move
- `SPACE` - Place bomb

**Player 2:**
- `Arrow Keys` - Move
- `ENTER` - Place bomb

**General:**
- `ESC` - Pause / Return to menu
- `R` - Restart (when game over)

### Objective
- Destroy walls with bombs
- Collect power-ups
- Eliminate enemies
- Defeat the other player (in PvP modes)
- Survive and get the highest score!

---

## ✨ Features

### Core Gameplay
- ✅ Classic Bomberman mechanics
- ✅ Bomb placement with timer
- ✅ 4-directional explosion propagation
- ✅ Player death on explosion or enemy contact

### Map System
- ✅ **3 Wall Types:**
  - Unbreakable Walls (permanent obstacles)
  - Breakable Walls (destroyed in 1 hit)
  - Hard Walls (require 3 hits)
  
- ✅ **3 Themes:**
  - Desert Theme (sand and stone)
  - Forest Theme (green and trees)
  - City Theme (concrete and brick)

### Power-Up System
- ✅ Bomb Count Increase
- ✅ Bomb Power Increase
- ✅ Speed Boost
- ✅ Skateboard (extra speed)
- ✅ Wall Pass (walk through breakable walls)

### Enemy AI System
- ✅ **Static AI:** Random movement
- ✅ **Chasing AI:** Follows nearest player
- ✅ **Intelligent AI:** A* pathfinding (BONUS +5)

### Database Features
- ✅ User registration and authentication
- ✅ Game statistics tracking (wins, losses, total games)
- ✅ Leaderboard system with top 10 scores
- ✅ User preferences (theme selection)

### Network Features
- ✅ Client-server architecture
- ✅ Real-time game synchronization
- ✅ Automatic player matching
- ✅ Lobby system (BONUS +5)

---

## 📁 Project Structure

```
bomberman/
├── main.py                      # Main entry point
├── config.py                    # Game configuration
├── requirements.txt             # Python dependencies
│
├── models/                      # Model Layer (MVC)
│   ├── player.py               # Player entity
│   ├── bomb.py                 # Bomb and Explosion entities
│   ├── wall.py                 # Wall entities
│   ├── powerup.py              # PowerUp entities
│   └── enemy.py                # Enemy entity
│
├── views/                       # View Layer (MVC)
│   ├── game_view.py            # Game rendering
│   ├── menu_view.py            # Menu screens
│   └── leaderboard_view.py     # Leaderboard screen
│
├── controllers/                 # Controller Layer (MVC)
│   ├── game_controller.py      # Game logic controller
│   └── network_controller.py   # Network game controller
│
├── patterns/                    # Design Patterns
│   ├── creational/
│   │   ├── factory.py          # Factory Method Pattern
│   │   └── singleton.py        # Singleton Pattern
│   ├── structural/
│   │   ├── decorator.py        # Decorator Pattern
│   │   └── facade.py           # Facade Pattern
│   └── behavioral/
│       ├── strategy.py         # Strategy Pattern
│       ├── observer.py         # Observer Pattern
│       └── state.py            # State Pattern
│
├── database/                    # Database Layer
│   ├── repository.py           # Base Repository
│   ├── user_repository.py      # User Repository
│   └── game_repository.py      # Game Repository
│
├── network/                     # Network Layer
│   ├── server.py               # Game server
│   └── client.py               # Game client
│
└── docs/                        # Documentation
    ├── design_document.pdf     # Design document
    └── uml_diagrams/           # UML diagrams
```

---

## 🗄️ Database Schema

```sql
-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Game statistics
CREATE TABLE game_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    total_games INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Leaderboard
CREATE TABLE leaderboard (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    score INT NOT NULL,
    game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- User preferences
CREATE TABLE user_preferences (
    pref_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    theme VARCHAR(20) DEFAULT 'desert',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

---

### 1. A* Pathfinding Algorithm 
**Location:** `patterns/behavioral/strategy.py` - `IntelligentAIStrategy`

Implements the A* pathfinding algorithm for intelligent enemy AI that finds the shortest path to the player.

**Features:**
- Heuristic-based path calculation
- Obstacle avoidance
- Dynamic recalculation
- Optimized performance with iteration limits

### 2. Professional UI/UX 
**Features:**
- Animated menu screens
- Smooth transitions
- Visual feedback for all actions
- Loading screens
- Professional color scheme
- Particle effects on explosions
- Health bars for hard walls
- Floating power-ups
- Player state visual indicators

### 3. Multiplayer Lobby System 
**Location:** `network/server.py`, `network/client.py`

Complete multiplayer infrastructure with:
- Automatic player matching
- Waiting room system
- Real-time game synchronization
- Connection management
- Graceful disconnect handling

---

##  Testing

### Running Tests

**Pattern Tests:**
```bash
python patterns/creational/singleton.py
python patterns/creational/factory.py
python patterns/behavioral/observer.py
python patterns/behavioral/strategy.py
```

**Repository Tests:**
```bash
python test/test_repository.py
```

**Network Tests:**
```bash
# Terminal 1
python network/server.py

# Terminal 2
python network/client.py
```

---

## 🐛 Known Issues & Future Improvements

### Known Issues
- Online multiplayer requires both clients to be on same network or port forwarding

### Future Improvements
- Implement more power-up types
- Add more map themes
- Tournament mode with brackets
- Replay system
- Mobile version

---

## 📚 References

1. Eric Freeman, Elisabeth Robson, Bert Bates, and Kathy Sierra. *Head First Design Patterns: A Brain-Friendly Guide*. O'Reilly Media, Inc., 2004.

2. Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides. *Design Patterns: Elements of Reusable Object-Oriented Software*. 1995.

3. Robert Nystrom. *Game Programming Patterns*. https://gameprogrammingpatterns.com/

4. Refactoring.Guru. *Design Patterns*. https://refactoring.guru/

5. SourceMaking. *Design Patterns*. https://sourcemaking.com/design_patterns

---

## 📝 License

This project is created for educational purposes as part of the Design Patterns course at İzmir Katip Çelebi University.

---

## 👏 Acknowledgments

- Prof. Dr. Doğan Aydın for the course and project guidance
- İzmir Katip Çelebi University
- The Pygame community
- All design pattern references and resources

---


