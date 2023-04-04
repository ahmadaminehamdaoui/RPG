from classes.maths.camera import camera
from classes.tiles.tileManager import tileManager
from classes.tiles.worldgen import perlin_gen, prop_gen
from classes.spriteManager import spriteManager

class Tilesheet:
    def __init__(self):
        self.tileLayer = []
        self.propLayer = []
        self.tileEntityLayer = []

        #
        self.hiddenDrawnTiles = 2
    
    def get_width(self):
        return len(self.tileLayer[0])

    def get_height(self):
        return len(self.tileLayer) 
    
    def get_tileID(self, x, y):
        try:
            return self.tileLayer[y][x][0].tileID
        except:
            return 'None'    

    def get_propID(self, x, y):
        try:
            return self.propLayer[y][x].propID
        except:
            return 'None'

    def is_solid(self, x, y):
        try:
            return self.tileLayer[y][x][0].is_solid()
        except:
            return False

    def draw(self, screen):
        minX = int(camera.pos.x//spriteManager.tileSize)-self.hiddenDrawnTiles
        maxX = int(camera.pos.x//spriteManager.tileSize)+(camera.w//spriteManager.tileSize)+self.hiddenDrawnTiles
        minY = int(camera.pos.y//spriteManager.tileSize)-self.hiddenDrawnTiles
        maxY = int(camera.pos.y//spriteManager.tileSize)+(camera.h//spriteManager.tileSize)+self.hiddenDrawnTiles
        for y in range(minY,maxY):
            for x in range(minX,maxX):
                if x < self.get_width() and y < self.get_height() and x >= 0 and y >= 0:
                    if ts.tileLayer[y][x][0].tileID == 'sand':
                        screen.blit(ts.tileLayer[y][x][0].sprite, (x*spriteManager.tileSize-4-camera.pos.x, y*spriteManager.tileSize-camera.pos.y-4))
        for y in range(minY,maxY):
            for x in range(minX,maxX):
                if x < self.get_width() and y < self.get_height() and x >= 0 and y >= 0:
                    screen.blit(ts.tileLayer[y][x][0].sprite, (x*spriteManager.tileSize-camera.pos.x, y*spriteManager.tileSize-camera.pos.y))
                    if ts.propLayer[y][x].propID != '0': 
                        screen.blit(ts.propLayer[y][x].sprite, (x*spriteManager.tileSize-camera.pos.x, y*spriteManager.tileSize-camera.pos.y))
                    if ts.tileLayer[y][x][1] != '':
                        screen.blit(spriteManager.get_tileEntitySprite(ts.tileLayer[y][x][1]), (x*spriteManager.tileSize-camera.pos.x, y*spriteManager.tileSize-camera.pos.y-spriteManager.get_tileEntitySprite(ts.tileLayer[y][x][1]).get_height()+spriteManager.tileSize))
    def gen(self, dim=(256,256), scale=25, octaves=2, lacunarity=2.0, persistence=1.2):
        self.tileLayer = perlin_gen(dim)
        self.propLayer = prop_gen(self)
    
ts = Tilesheet()
print('\nGenerating map...')
ts.gen(dim=(128,128))
print('Done!')