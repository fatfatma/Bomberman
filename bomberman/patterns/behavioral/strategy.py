# patterns/behavioral/strategy.py
"""
Strategy Pattern - Enemy AI Behaviors
Different AI strategies for enemy movement
"""

from abc import ABC, abstractmethod
import random
import math


class AIStrategy(ABC):
    """
    Abstract strategy interface for enemy AI.
    All AI strategies must implement calculate_move method.
    """

    @abstractmethod
    def calculate_move(self, enemy, walls, players, enemies):
        """
        Calculate the next move for the enemy.

        Args:
            enemy (Enemy): The enemy to move
            walls (list): List of walls
            players (list): List of players
            enemies (list): List of other enemies

        Returns:
            tuple: (dx, dy) direction to move
        """
        pass


class StaticAIStrategy(AIStrategy):
    """
    Static AI - Moves in random directions.
    Changes direction randomly or when hitting obstacles.
    """

    def __init__(self):
        self.current_direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.steps_in_direction = 0
        self.max_steps = random.randint(20, 50)

    def calculate_move(self, enemy, walls, players, enemies):
        """Move in current direction, change randomly"""
        self.steps_in_direction += 1

        # Change direction randomly or after max steps
        if self.steps_in_direction >= self.max_steps or random.random() < 0.05:
            self.current_direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            self.steps_in_direction = 0
            self.max_steps = random.randint(20, 50)

        return self.current_direction


class ChasingAIStrategy(AIStrategy):
    """
    Chasing AI - Follows the nearest player.
    Uses simple distance calculation to chase players.
    """

    def calculate_move(self, enemy, walls, players, enemies):
        """Move towards the nearest alive player"""
        # Find nearest player
        nearest_player = None
        min_distance = float('inf')

        for player in players:
            if player.state_manager.is_alive():
                distance = math.sqrt(
                    (enemy.grid_x - player.grid_x) ** 2 +
                    (enemy.grid_y - player.grid_y) ** 2
                )
                if distance < min_distance:
                    min_distance = distance
                    nearest_player = player

        if nearest_player is None:
            return (0, 0)

        # Calculate direction towards player
        dx = 0
        dy = 0

        if enemy.grid_x < nearest_player.grid_x:
            dx = 1
        elif enemy.grid_x > nearest_player.grid_x:
            dx = -1

        if enemy.grid_y < nearest_player.grid_y:
            dy = 1
        elif enemy.grid_y > nearest_player.grid_y:
            dy = -1

        # Move in one direction at a time (prefer horizontal or vertical)
        if random.random() < 0.5 and dx != 0:
            return (dx, 0)
        elif dy != 0:
            return (0, dy)
        elif dx != 0:
            return (dx, 0)

        return (0, 0)


class IntelligentAIStrategy(AIStrategy):
    """
    Intelligent AI - Uses A* pathfinding algorithm.
    Finds the shortest path to the nearest player.
    """

    def __init__(self):
        self.path = []
        self.recalculate_timer = 0
        self.recalculate_interval = 500  # Recalculate path every 500ms

    def calculate_move(self, enemy, walls, players, enemies):
        """Use A* pathfinding to move towards nearest player"""
        self.recalculate_timer += 16  # Approximate frame time

        # Recalculate path periodically
        if self.recalculate_timer >= self.recalculate_interval or not self.path:
            self.path = self._find_path(enemy, walls, players)
            self.recalculate_timer = 0

        # Follow the path
        if self.path and len(self.path) > 1:
            next_pos = self.path[1]  # Next position in path

            dx = 0
            dy = 0

            if next_pos[0] > enemy.grid_x:
                dx = 1
            elif next_pos[0] < enemy.grid_x:
                dx = -1

            if next_pos[1] > enemy.grid_y:
                dy = 1
            elif next_pos[1] < enemy.grid_y:
                dy = -1

            # Check if reached next position
            if enemy.grid_x == next_pos[0] and enemy.grid_y == next_pos[1]:
                self.path.pop(0)  # Remove reached position

            return (dx, dy)

        return (0, 0)

    def _find_path(self, enemy, walls, players):
        """
        A* pathfinding algorithm implementation.

        Returns:
            list: List of (x, y) grid positions representing the path
        """
        # Find nearest alive player
        nearest_player = None
        min_distance = float('inf')

        for player in players:
            if player.state_manager.is_alive():
                distance = math.sqrt(
                    (enemy.grid_x - player.grid_x) ** 2 +
                    (enemy.grid_y - player.grid_y) ** 2
                )
                if distance < min_distance:
                    min_distance = distance
                    nearest_player = player

        if nearest_player is None:
            return []

        # A* algorithm
        start = (enemy.grid_x, enemy.grid_y)
        goal = (nearest_player.grid_x, nearest_player.grid_y)

        # Create wall grid for faster lookup
        wall_grid = set()
        for wall in walls:
            if not wall.destroyed:
                wall_grid.add((wall.grid_x, wall.grid_y))

        # A* implementation
        open_set = [start]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, goal)}

        max_iterations = 100  # Prevent infinite loops
        iterations = 0

        while open_set and iterations < max_iterations:
            iterations += 1

            # Find node with lowest f_score
            current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))

            if current == goal:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            open_set.remove(current)

            # Check neighbors
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)

                # Skip if wall
                if neighbor in wall_grid:
                    continue

                # Skip if out of bounds
                if neighbor[0] < 0 or neighbor[0] >= 20 or neighbor[1] < 0 or neighbor[1] >= 15:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, goal)

                    if neighbor not in open_set:
                        open_set.append(neighbor)

        # No path found, return empty
        return []

    def _heuristic(self, pos1, pos2):
        """Manhattan distance heuristic"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# Factory function for creating AI strategies
def create_ai_strategy(ai_type):
    """
    Factory function to create AI strategies.

    Args:
        ai_type (str): Type of AI ('static', 'chasing', 'intelligent')

    Returns:
        AIStrategy: Appropriate AI strategy object
    """
    if ai_type == 'static':
        return StaticAIStrategy()
    elif ai_type == 'chasing':
        return ChasingAIStrategy()
    elif ai_type == 'intelligent':
        return IntelligentAIStrategy()
    else:
        raise ValueError(f"Unknown AI type: {ai_type}")


# Usage Example
if __name__ == "__main__":
    print("=== Testing Strategy Pattern ===\n")

    # Create different AI strategies
    static_ai = create_ai_strategy('static')
    chasing_ai = create_ai_strategy('chasing')
    intelligent_ai = create_ai_strategy('intelligent')

    print(f"✅ Created {static_ai.__class__.__name__}")
    print(f"✅ Created {chasing_ai.__class__.__name__}")
    print(f"✅ Created {intelligent_ai.__class__.__name__}")

    print("\n✅ Strategy Pattern test completed!")
    print("\nAI Strategies:")
    print("  - Static: Random movement")
    print("  - Chasing: Follows nearest player")
    print("  - Intelligent: A* pathfinding (BONUS +5)")