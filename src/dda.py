import math
from core import Player, GameMap

class RayResult:
    def __init__(self, hit_point, hit_dist, first_distX, first_distY):
        self.hit = hit_point
        self.hit_dist = hit_dist
        self.first_distX = first_distX
        self.first_distY = first_distY

def sign(number):
    if number == 0:
        return 0
    elif number < 0:
        return -1
    else:
        return 1

def dda(player: Player, game_map: GameMap):    
    # we must calculate the distance if y += 1 and if x += 1
    # if the denominator is zero this means we're moving in a perfect horizontal or vertical movement
    if player.dir.x == 0 and player.dir.y == 0:
        return (RayResult((player.pos.x, player.pos.y), None, None, None))
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
    first_distX = first_distY = None
    mapX = int(player.pos.x)
    mapY = int(player.pos.y)

    stepX = sign(player.dir.x)
    stepY = sign(player.dir.y)
    side = None
    while not game_map.is_wall(mapX, mapY):
        if distY < distX:
            if first_distY is None:
                first_distY = distY
            mapY += stepY
            distY += distBetweenRows
            side = 1
        else:
            if first_distX is None:
                first_distX = distX
            mapX += stepX
            distX += distBetweenCols
            side = 0
    if side is None:
        final_dest = 0
    elif side == 1:
        final_dest = distY - distBetweenRows
    else:
        final_dest = distX - distBetweenCols
    normalized_dir = player.dir.normalize()
    hit_x = player.pos.x + (normalized_dir.x * final_dest)
    hit_y = player.pos.y + (normalized_dir.y * final_dest)

    return RayResult((hit_x, hit_y), final_dest, first_distX, first_distY)