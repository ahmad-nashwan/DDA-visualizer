import pygame
import math
from core import Vec2D, GameMap, Player, Direction, CELL_SIZE

def sign(number):
    if number == 0:
        return 0
    elif number < 0:
        return -1
    else:
        return 1
    
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

def draw_line_of_sight(screen, player: Player, x, y):
    x *= CELL_SIZE
    y *= CELL_SIZE
    player_x = player.pos.x * CELL_SIZE
    player_y = player.pos.y * CELL_SIZE
    pygame.draw.line(screen, pygame.Color("white"), (player_x, player_y), (x, y), 1)


def dda(screen, player: Player, game_map: GameMap):
    visited = []
    # store the current cell as visited
    visited.append(player.pos.get_floored().to_tuple())
    # before doing anything, we link the direction with the cursor as a vector
    mouse_pos = Vec2D.from_tuple(pygame.mouse.get_pos()).scale(1 / CELL_SIZE)
    # how to get from player to mouse? subtraction
    player.dir = mouse_pos - player.pos
    # after that we must calculate the distance if y += 1 and if x += 1
    # if the denominator is zero this means we're moving in a perfect horizontal or vertical movement
    # bug 1 here
    if player.dir.y == 0:
        distBetweenRows = math.inf
    else:
        distBetweenRows = math.sqrt(1 + (player.dir.x / player.dir.y) ** 2)
    if player.dir.x == 0:
        distBetweenCols = math.inf
    else:
        distBetweenCols = math.sqrt(1 + (player.dir.y / player.dir.x) ** 2)
    # we figure out where we're starting now
    fractional_pos = player.pos - player.pos.get_floored()
    if player.dir.x < 0:
        distX = fractional_pos.x * distBetweenCols
    else:
        distX = (1 - fractional_pos.x) * distBetweenCols
    if player.dir.y < 0:
        distY = fractional_pos.y * distBetweenRows
    else:
        distY = (1 - fractional_pos.y) * distBetweenRows
    # the ray starts at the players position
    mapX = int(player.pos.x)
    mapY = int(player.pos.y)
    # Fix 2: Cache the step directions before the loop
    stepX = sign(player.dir.x)
    stepY = sign(player.dir.y)
    side = None
    while not game_map.is_wall(mapX, mapY):
        if distY < distX:
            mapY += stepY
            distY += distBetweenRows
            side = 1
        else:
            mapX += stepX
            distX += distBetweenCols
            side = 0
        visited.append((mapX, mapY))  

    if side is None:
        final_dest = 0
    elif side == 1:
        final_dest = distY - distBetweenRows
    else:
        final_dest = distX - distBetweenCols

    normalized_dir = player.dir.normalize()
    hit_x = player.pos.x + (normalized_dir.x * final_dest)
    hit_y = player.pos.y + (normalized_dir.y * final_dest)

    print(visited[-1])
    draw_line_of_sight(screen, player, hit_x, hit_y)


def start_visualization(game_map):
    pygame.init()
    screen = pygame.display.set_mode((1024, 600))
    pygame.display.set_caption("DDA visualizer")
    clock = pygame.time.Clock()
    running = True
    player = Player(Vec2D(8, 7))
    pygame.mouse.set_visible(False)

    velocity = 0.09
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
        dda(screen, player, game_map)
        draw_cursor(screen)
        draw_player(screen, player)
        pygame.display.update()
        clock.tick(60)

    pygame.QUIT

def main():
    grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    game_map = GameMap(grid)
    start_visualization(game_map)


if __name__ == "__main__":
    main()
