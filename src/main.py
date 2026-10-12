import pygame
import random
import render
from core import Vec2D, GameMap, Player, Direction
from dda import dda, RayResult


def set_starting_pos(game_map: GameMap):
    x = random.uniform(0, game_map.width -1)
    y = random.uniform(0, game_map.height - 1)
    while game_map.is_wall(x, y):    
        x = random.uniform(0, game_map.width -1)
        y = random.uniform(0, game_map.height - 1)
    return Vec2D(x, y)


def set_player_dir(player: Player, camera: render.Camera):
    x, y = pygame.mouse.get_pos()
    mouse_pos = Vec2D.from_tuple(camera.to_grid(x, y))
    player.dir = mouse_pos - player.pos


def start_visualization(game_map):
    pygame.init()
    camera = render.Camera(64, 1024, 640)
    screen = pygame.display.set_mode((camera.screen_width, camera.screen_height))
    pygame.display.set_caption("DDA visualizer")
    clock = pygame.time.Clock()
    font = render.create_font()
    player = Player(set_starting_pos(game_map))
    pygame.mouse.set_visible(False)
    velocity = 0.02

    running = True
    detailed_mode = True
    camera.update(player, detailed_mode)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                detailed_mode = not detailed_mode
                if detailed_mode:
                    velocity = 0.02
                else:
                    velocity = 0.08
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.move(game_map,Direction.UP ,velocity)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.move(game_map, Direction.LEFT, velocity)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.move(game_map, Direction.DOWN, velocity)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.move(game_map, Direction.RIGHT, velocity)

        camera.update(player, detailed_mode)
        screen.fill(render.BACKGROUND)
        render.draw_grid(screen, camera, game_map.grid)
        set_player_dir(player, camera)
        ray = dda(player, game_map)
        render.draw_line_of_sight(screen, camera, player, ray.hit)
        render.draw_hit_point(screen, camera, ray.hit)
        if detailed_mode and ray.first_distX is not None:
            render.draw_crossing(screen, camera, player, ray.first_distX, render.CROSSING_X)
        if detailed_mode and ray.first_distY is not None:
            render.draw_crossing(screen, camera, player, ray.first_distY, render.CROSSING_Y)
        render.draw_player(screen, camera, player)
        render.draw_legend(screen, font, detailed_mode)
        render.draw_cursor(screen)
        pygame.display.set_caption("Detailed Mode" if detailed_mode else "Free mode")
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
