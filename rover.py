# rover.py

class Rover:
    def __init__(self, x=0, y=0, direction='N', grid_size=(5, 5), terrain=None):
        # Set initial position of the rover
        self.x = x
        self.y = y
        self.direction = direction  # N = North, E = East, S = South, W = West
        self.grid_width, self.grid_height = grid_size
        # Order of directions (for turning)
        self.directions = ['N', 'E', 'S', 'W']

        # Set obstacles (e.g. rocks)
        if terrain is None:
            terrain = [(2, 2), (1, 3), (3, 1)]  # You can customize
        self.terrain = terrain
        self.history = [] # ← to track previous states

    def get_next_position(self):
        """Calculate next position based on direction"""
        if self.direction == 'N':
            return self.x, self.y + 1
        elif self.direction == 'E':
            return self.x + 1, self.y
        elif self.direction == 'S':
            return self.x, self.y - 1
        elif self.direction == 'W':
            return self.x - 1, self.y

    def move(self):
        """Try to move forward one step"""
        new_x, new_y = self.get_next_position()

        # Check if move is inside grid
        if not (0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height):
            return "🚧 Can't move — edge of the terrain!"

        # Check for obstacle
        if (new_x, new_y) in self.terrain:
            return "🪨 Obstacle detected! Move canceled."

        # Move is valid
        self.history.append((self.x, self.y, self.direction))  # Save current state
        self.x = new_x
        self.y = new_y
        return f"✅ Moved to ({self.x}, {self.y}) facing {self.direction}"


    def turn_left(self):
        self.history.append((self.x, self.y, self.direction))
        index = self.directions.index(self.direction)
        self.direction = self.directions[(index - 1) % 4]
        return f"↪️ Turned left, now facing {self.direction}"


    def turn_right(self):
        self.history.append((self.x, self.y, self.direction))
        index = self.directions.index(self.direction)
        self.direction = self.directions[(index + 1) % 4]
        return f"↩️ Turned right, now facing {self.direction}"


    def status(self):
        return f"📍 Position: ({self.x}, {self.y}) | Facing: {self.direction}"
    
    def undo(self):
        if self.history:
            self.x, self.y, self.direction = self.history.pop()
            return "↩️ Undid last move"
        return "❌ Nothing to undo"

    def reset(self):
        self.x, self.y, self.direction = 0, 0, 'N'
        self.history.clear()
        return "🔄 Reset to start"
    
    def display_map(self):
        print("\n🗺️  Mars Terrain Map:")
        for y in reversed(range(self.grid_height)):
            row = ""
            for x in range(self.grid_width):
                if (x, y) == (self.x, self.y):
                    row += "🤖 "
                elif (x, y) in self.terrain:
                    row += "🪨 "
                else:
                    row += "⬜ "
            print(row)
        print()

