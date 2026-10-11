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