from pygame import image as pyimage
from pygame import transform as pytransform
from classes.spriteManager import spriteManager

class TileManager:
    def __init__(self): 
        # tile IDs : empty, water, sand, grass, mountain
        pass

    def set_tileSize(self, ts, tileSize):
        spriteManager.tileSize = tileSize
        spriteManager.reset('tiles')
        for y in range(ts.get_height()):
            for x in range(ts.get_width()):
                ts.tileLayer[y][x].update(ts.tileLayer, x, y)


tileManager = TileManager()