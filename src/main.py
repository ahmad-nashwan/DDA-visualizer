import pygame
import random
from core import Vec2D, GameMap, Player, Direction, CELL_SIZE
from dda import dda
    
def draw_grid(screen, grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, pygame.Color("white"), rect)
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
            color = pygame.Color("blue") if grid[row][col] == 1 else pygame.Color("black")
            pygame.draw.rect(screen, color, rect)

def draw_player(screen, player: Player):
    pygame.draw.circle(screen, pygame.Color("red"), (player.pos.x * CELL_SIZE, player.pos.y * CELL_SIZE), 8)

def draw_cursor(screen):
    x, y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, pygame.Color("green"), (x, y), 8)

def draw_line_of_sight(screen, player: Player, position: tuple):
    x = position[0] * CELL_SIZE
    y = position[1] * CELL_SIZE
    player_x = player.pos.x * CELL_SIZE
    player_y = player.pos.y * CELL_SIZE
    pygame.draw.line(screen, pygame.Color("white"), (player_x, player_y), (x, y), 1)

def set_starting_pos(game_map: GameMap):
    x = random.uniform(0, game_map.width -1)
    y = random.uniform(0, game_map.height - 1)
    while game_map.is_wall(x, y):    
        x = random.uniform(0, game_map.width -1)
        y = random.uniform(0, game_map.height - 1)
    return Vec2D(x, y)

def set_player_dir(player: Player):
    mouse_pos = Vec2D.from_tuple(pygame.mouse.get_pos()).scale(1 / CELL_SIZE)
    player.dir = mouse_pos - player.pos

def start_visualization(game_map):
    pygame.init()
    screen = pygame.display.set_mode((1024,640))
    pygame.display.set_caption("DDA visualizer")
    clock = pygame.time.Clock()
    player = Player(set_starting_pos(game_map))
    pygame.mouse.set_visible(False)
    velocity = 0.09

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(game_map,Direction.UP ,velocity)
        if keys[pygame.K_a]:
            player.move(game_map, Direction.LEFT, velocity)
        if keys[pygame.K_s]:
            player.move(game_map, Direction.DOWN, velocity)
        if keys[pygame.K_d]:
            player.move(game_map, Direction.RIGHT, velocity)

        draw_grid(screen, game_map.grid)
        set_player_dir(player)
        hit_point = dda(player, game_map)
        draw_line_of_sight(screen, player, hit_point)
        draw_cursor(screen)
        draw_player(screen, player)
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
