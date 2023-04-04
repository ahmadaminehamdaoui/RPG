# MODULES
import pygame, sys
from math import sqrt, radians, cos, sin
from classes.maths.vector2 import Vector2
from classes.spriteManager import spriteManager

# SPRITES
def color_surface(surface, rgb):
    surface = surface.copy()
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,0] = rgb[0]
    arr[:,:,1] = rgb[1]
    arr[:,:,2] = rgb[2]
    return surface

# POSITIONS
def get_tile_position(pos):
    if type(pos) == list or type(pos) == tuple:
        return (int(pos[0]//spriteManager.tileSize), int(pos[1]//spriteManager.tileSize))
    else:
        return Vector2(int(pos.x//spriteManager.tileSize), int(pos.y//spriteManager.tileSize))

def dist(p1,p2):
    return sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)

# COLLISIONS
def is_colliding(pos1, w1, h1, pos2, w2, h2):
    w1 -= 1
    h1 -= 1
    w2 -= 1
    h2 -= 1
    return pos2.x+w2 > pos1.x and pos2.y+h2 > pos1.y and pos1.x+w1 > pos2.x and pos1.y+h1 > pos2.y

def is_circle_colliding(pos1, radius1, pos2, radius2):
    distanceSquared = (pos2.x-pos1.x)**2+(pos2.y-pos1.y)**2
    if distanceSquared < (radius1+radius2)**2:
        return True
    return False
    
def is_point_colliding(point, rect, width):
    width -= 1
    # 3EME ET + A FINIR
    if point[0]<rect[0]+width and point[0]>rect[0] and point[1]<rect[1]+width and point[1]>rect[1]:
        return True
    return False