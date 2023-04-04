from pygame import display
from classes.maths.camera import camera

def relative_blit(sprite, pos, screen):
    screen.blit(sprite, (pos.x-camera.pos.x, pos.y-camera.pos.y))