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
LABEL_BRIGHT = pygame.Color("#737aa2")

FONT_SIZE = 16
PANEL_MARGIN = 16
PANEL_PADDING = 14
PANEL_SWATCH_RADIUS = 5
PANEL_TEXT_COLUMN = 22
PANEL_LINE_GAP = 8
PANEL_OPACITY = 170  # 0 is invisible, 255 is solid

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

def create_font():
    return pygame.font.SysFont("monospace", FONT_SIZE, bold=True)


def draw_legend(screen, font, detailed_mode: bool):
    rows = [(PLAYER, "player")]
    if detailed_mode:
        rows.append((CROSSING_X, "first intersection with a vertical line"))
        rows.append((CROSSING_Y, "first intersection with a horizontal line"))
    rows.append((HIT_POINT, "where the ray hits a wall"))
    if detailed_mode:
        hint = "press M for free mode"
    else:
        hint = "press M for detailed mode"

    line_height = font.get_linesize() + PANEL_LINE_GAP
    text_width = max(font.size(text)[0] for color, text in rows)
    width = PANEL_PADDING * 2 + max(PANEL_TEXT_COLUMN + text_width, font.size(hint)[0])
    # one extra line for the hint, and a gap above it
    height = PANEL_PADDING * 2 + line_height * (len(rows) + 1)
    panel = pygame.Surface((width, height), pygame.SRCALPHA)
    panel.fill((BACKGROUND.r, BACKGROUND.g, BACKGROUND.b, PANEL_OPACITY))
    pygame.draw.rect(panel, WALL_EDGE, panel.get_rect(), 1)
    for i, (color, text) in enumerate(rows):
        y = PANEL_PADDING + i * line_height
        swatch_center = (PANEL_PADDING + PANEL_SWATCH_RADIUS, y + font.get_linesize() // 2)
        pygame.draw.circle(panel, color, swatch_center, PANEL_SWATCH_RADIUS)
        panel.blit(font.render(text, True, TEXT), (PANEL_PADDING + PANEL_TEXT_COLUMN, y))
    hint_y = PANEL_PADDING + len(rows) * line_height + PANEL_LINE_GAP
    panel.blit(font.render(hint, True, LABEL_BRIGHT), (PANEL_PADDING, hint_y))
    screen.blit(panel, (PANEL_MARGIN, PANEL_MARGIN))
