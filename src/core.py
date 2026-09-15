import math
from enum import Enum

CELL_SIZE = 32

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

class Direction(Enum):
    # (x, y) -> according to pygame
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

class GameMap:
    def __init__(self, grid):
        if not grid or len(grid) < 1:
            raise Exception # do something lol
        self.width = len(grid[0])
        self.height = len(grid)
        self.grid = grid

    def is_wall(self, x, y):
        x = math.floor(x)
        y = math.floor(y)
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        if self.grid[x][y] == 1:
            return True
        return False

class Player:
    def __init__(self, pos, dir=None):
        self.pos = pos
        self.dir = dir if dir else Vec2D(1, 0)

    def move(self, game_map:GameMap, movement_dir: Direction, velocity:int):
        x, y = movement_dir.value
        new_x = self.pos.x + x * velocity
        new_y = self.pos.y + y * velocity

        if not game_map.is_wall(new_x, self.pos.y):
            self.pos.x = new_x
        if not game_map.is_wall(self.pos.x, new_y):
            self.pos.y = new_y
