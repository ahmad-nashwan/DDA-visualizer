import pygame
from core import Player

# collor pallete
BACKGROUND = pygame.Color("#16161e")
FLOOR = pygame.Color("#1a1b26")
GRID_LINE = pygame.Color("#292e42")
WALL = pygame.Color("#3b4261")
WALL_EDGE = pygame.Color("#565f89")
VISITED = pygame.Color(125, 207, 255, 51)  # ray colour at 20% opacity
RAY = pygame.Color("#7dcfff")
PLAYER = pygame.Color("#7aa2f7")
HIT_POINT = pygame.Color("#f7768e")
CURSOR = pygame.Color("#9ece6a")
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
            target_scale = self.cell_size * 3
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