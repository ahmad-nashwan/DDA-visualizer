import math
from core import Player, GameMap

def sign(number):
    if number == 0:
        return 0
    elif number < 0:
        return -1
    else:
        return 1
    
def dda(player: Player, game_map: GameMap):
    visited = []
    # store the current cell as visited
    visited.append(player.pos.get_floored().to_tuple())
    
    # after that we must calculate the distance if y += 1 and if x += 1
    # if the denominator is zero this means we're moving in a perfect horizontal or vertical movement
    # bug 1 here
    if player.dir.x == 0 and player.dir.y == 0:
        return (player.pos.x, player.pos.y)
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
    return (hit_x, hit_y)