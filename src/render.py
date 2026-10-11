import pygame
from core import Player, GameMap

# cool collor pallete
BACKGROUND = pygame.Color("#16161e")
FLOOR = pygame.Color("#1a1b26")
GRID_LINE = pygame.Color("#292e42")
WALL = pygame.Color("#3b4261")
WALL_EDGE = pygame.Color("#565f89")
VISITED = pygame.Color(125, 207, 255, 51) 
RAY = pygame.Color("#3cb1f5")
PLAYER = pygame.Color("#7aa2f7")
HIT_POINT = pygame.Color("#f7768e")
CURSOR = pygame.Color("#70736c")
CROSSING_X = pygame.Color("#ff9e64")
CROSSING_Y = pygame.Color("#bb9af7")
TEXT = pygame.Color("#c0caf5")
LABEL = pygame.Color("#565f89")

class Camera:
    def __init__(self, cell_size, screen_width, screen_height):
        self.cell_size = cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale = self.cell_size
        self.offset_x = 0
        self.offset_y = 0

    def update(self, player: Player, detailed_mode: bool):
        if detailed_mode:
            target_scale = self.cell_size * 4
            target_offset_x = (self.screen_width / 2) - (player.pos.x * target_scale)
            target_offset_y = (self.screen_height / 2) - (player.pos.y * target_scale)
        else:
            target_scale = self.cell_size
            target_offset_x = 0
            target_offset_y = 0

        # adding smooth zoom
        speed = 0.15
        # here we subtract to not increment infinitely
        self.scale += (target_scale - self.scale) * speed
        self.offset_x += (target_offset_x - self.offset_x)* speed
        self.offset_y += (target_offset_y - self.offset_y) * speed
        # smooth operatorrrrrr

    def to_pixels(self, x, y):
        return (x * self.scale + self.offset_x, y * self.scale + self.offset_y)

    def to_grid(self, x, y):
        return ((x - self.offset_x) / self.scale, (y - self.offset_y) / self.scale)


def draw_grid(screen, camera: Camera, grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            x, y = camera.to_pixels(col, row)
            rect = pygame.Rect(x, y, camera.scale, camera.scale)
            pygame.draw.rect(screen, GRID_LINE, rect)
            rect = pygame.Rect(x, y, camera.scale - 1, camera.scale - 1)
            color = WALL if grid[row][col] == 1 else FLOOR
            pygame.draw.rect(screen, color, rect)
            if grid[row][col] == 1:
                pygame.draw.rect(screen, WALL_EDGE, rect, 2)

def draw_player(screen, camera: Camera, player: Player):
    pygame.draw.circle(screen, PLAYER, camera.to_pixels(player.pos.x, player.pos.y), 8)

def draw_cursor(screen):
    x, y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, CURSOR, (x, y), 5)

def draw_line_of_sight(screen, camera: Camera, player: Player, position: tuple):
    x, y = camera.to_pixels(position[0], position[1])
    player_x, player_y = camera.to_pixels(player.pos.x, player.pos.y)
    pygame.draw.line(screen, RAY, (player_x, player_y), (x, y), 1)

def draw_hit_point(screen, camera: Camera, position: tuple):
    pygame.draw.circle(screen, HIT_POINT, camera.to_pixels(position[0], position[1]), 5)

def draw_crossing(screen, camera: Camera, player: Player, distance, color):
    direction = player.dir.normalize()
    x = player.pos.x + direction.x * distance
    y = player.pos.y + direction.y * distance
    pygame.draw.circle(screen, color, camera.to_pixels(x, y), 6)