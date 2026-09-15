import math

class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vec2D(self.x * other.x, self.y * other.y)

    def rotate(self, angle):
        return Vec2D(math.cos(angle) * self.x - math.sin(angle) * self.y,
                     math.sin(angle) * self.x + math.cos(angle) * self.y)
    
    def scale(self, scaler):
        return Vec2D(self.x * scaler, self.y * scaler)

class GameMap:
    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.grid = grid

    def is_wall(self, x, y):
        x = math.floor(x)
        y = math.floor(y)
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        if self.grid[x, y] == 1:
            return True
        return False

class Player:
    def __init__(self, pos, dir=None):
        self.pos = pos
        self.dir = dir if dir else Vec2D(1, 0)

    def move(self, game_map, velocity):
        new_x = self.pos.x + self.dir.x * velocity
        new_y = self.pos.y + self.dir.y * velocity

        if not game_map.is_wall(new_x, self.pos.y):
            self.pos.x = new_x
        if not game_map.is_wall(self.pos.x, new_y):
            self.pos.y = new_y

    def strafe(self, game_map, velocity):
        strafe = Vec2D(-self.dir.y, self.dir.x)
        new_x = self.pos.x + strafe.x * velocity
        new_y = self.pos.y + strafe.y * velocity

        if not game_map.is_wall(new_x, self.pos.y):
            self.pos.x = new_x
        if not game_map.is_wall(self.pos.x, new_y):
            self.pos.y = new_y
