import pygame
import random
from core import Vec2D, GameMap, Player, Direction
from dda import dda
from render import Camera

def draw_grid(screen, camera: Camera, grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            x, y = camera.to_pixels(col, row)
            rect = pygame.Rect(x, y, camera.scale, camera.scale)
            pygame.draw.rect(screen, pygame.Color("white"), rect)
            rect = pygame.Rect(x, y, camera.scale - 1, camera.scale - 1)
            color = pygame.Color("blue") if grid[row][col] == 1 else pygame.Color("black")
            pygame.draw.rect(screen, color, rect)

def draw_player(screen, camera: Camera, player: Player):
    pygame.draw.circle(screen, pygame.Color("red"), camera.to_pixels(player.pos.x, player.pos.y), 8)

def draw_cursor(screen):
    x, y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, pygame.Color("green"), (x, y), 8)

def draw_line_of_sight(screen, camera: Camera, player: Player, position: tuple):
    x, y = camera.to_pixels(position[0], position[1])
    player_x, player_y = camera.to_pixels(player.pos.x, player.pos.y)
    pygame.draw.line(screen, pygame.Color("white"), (player_x, player_y), (x, y), 1)

def set_starting_pos(game_map: GameMap):
    x = random.uniform(0, game_map.width -1)
    y = random.uniform(0, game_map.height - 1)
    while game_map.is_wall(x, y):    
        x = random.uniform(0, game_map.width -1)
        y = random.uniform(0, game_map.height - 1)
    return Vec2D(x, y)

def set_player_dir(player: Player, camera: Camera):
    x, y = pygame.mouse.get_pos()
    mouse_pos = Vec2D.from_tuple(camera.to_grid(x, y))
    player.dir = mouse_pos - player.pos

def start_visualization(game_map):
    pygame.init()
    camera = Camera(64, 1024, 640)
    screen = pygame.display.set_mode((camera.screen_width, camera.screen_height))
    pygame.display.set_caption("DDA visualizer")
    clock = pygame.time.Clock()
    player = Player(set_starting_pos(game_map))
    pygame.mouse.set_visible(False)
    velocity = 0.08

    running = True
    detailed_mode = False
    camera.update(player, detailed_mode)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                detailed_mode = not detailed_mode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(game_map,Direction.UP ,velocity)
        if keys[pygame.K_a]:
            player.move(game_map, Direction.LEFT, velocity)
        if keys[pygame.K_s]:
            player.move(game_map, Direction.DOWN, velocity)
        if keys[pygame.K_d]:
            player.move(game_map, Direction.RIGHT, velocity)

        camera.update(player, detailed_mode)
        screen.fill("black")
        draw_grid(screen, camera, game_map.grid)
        set_player_dir(player, camera)
        hit_point = dda(player, game_map)
        draw_line_of_sight(screen, camera, player, hit_point)
        draw_cursor(screen)
        draw_player(screen, camera, player)
        pygame.display.set_caption("detailed" if detailed_mode else "free")
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def main():
    grid = [
            [1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1,1, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1,1, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1],
    ]
    game_map = GameMap(grid)
    start_visualization(game_map)


if __name__ == "__main__":
    main()
