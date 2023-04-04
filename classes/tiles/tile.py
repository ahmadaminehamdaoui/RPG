from classes.spriteManager import spriteManager

class Tile:
    def __init__(self, tileID, sprite=None):
        self.tileID = tileID
        self.sprite = sprite
    
    def set_tileID(self, tileID):
        self.tileID = tileID
    
    def update(self, tilesheet, x, y):
        if self.tileID == 'sand':
            sprite_path = 'LEFT_UP_RIGHT_DOWN'
        else:
            adjacentTiles = ''
            if x-1>=0:
                if tilesheet[y][x-1][0].tileID == self.tileID:
                    adjacentTiles += 'LEFT_'
            if y-1>=0:
                if tilesheet[y-1][x][0].tileID == self.tileID:
                    adjacentTiles += 'UP_'
            if x+1<len(tilesheet[0]):
                if tilesheet[y][x+1][0].tileID == self.tileID:
                    adjacentTiles += 'RIGHT_'
            if y+1<len(tilesheet):
                if tilesheet[y+1][x][0].tileID == self.tileID:
                    adjacentTiles += 'DOWN_'
            #---#
            if adjacentTiles == '': 
                sprite_path = 'NONE'
            else:
                sprite_path = adjacentTiles[0:-1]

        self.sprite = spriteManager.get_tileSprite(self.tileID, sprite_path)
    
    def is_solid(self):
        if self.tileID == 'mountain' or self.tileID == 'water':
            return True
        return False