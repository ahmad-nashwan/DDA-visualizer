from core import Player

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
            self.scale = self.cell_size * 3
            self.offset_x = (self.screen_width / 2) - (player.pos.x * self.scale)
            self.offset_y = (self.screen_height / 2) - (player.pos.y * self.scale)
        else:
            self.scale = self.cell_size
            self.offset_x = 0
            self.offset_y = 0

    def to_pixels(self, x, y):
        return (x * self.scale + self.offset_x, y * self.scale + self.offset_y)

    def to_grid(self, x, y):
        return ((x - self.offset_x) / self.scale, (y - self.offset_y) / self.scale)