from pygame import image as pyimage
from pygame import transform as pytransform
from random import randint

class SpriteManager:
    def __init__(self):
        self.tileSize = 48
        self.sprites = {'error':pytransform.scale(pyimage.load('./sprites/error.png'), (self.tileSize, self.tileSize)),
                        'tiles':{'sand':{'LEFT_UP_RIGHT_DOWN':pytransform.scale(pyimage.load('./sprites/tiles/sand/LEFT_UP_RIGHT_DOWN.png'), (self.tileSize+(self.tileSize//16)*2, self.tileSize+(self.tileSize//16)*2))}},
                        'props':{},
                        'entities':{},
                        'items':{},
                        'particles':{},
                        'tile_entities':{},
                        'misc':{}}
    
    def get_miscSprite(self, textureID, xscale=1, yscale=1):
        try:
            img = pyimage.load('./sprites/{}.png'.format(textureID))
            dims = (img.get_width(), img.get_height())
            return pytransform.scale(pyimage.load('./sprites/{}.png'.format(textureID)), (int(dims[0]*xscale), int(dims[1]*yscale)))
        except:
            return self.sprites['error']

    def get_particleSprite(self, particleID, scale=1):
        try:
            if particleID not in self.sprites['particles'].keys():
                self.sprites['particles'][particleID] = pytransform.scale(pyimage.load('./sprites/particles/{}.png'.format(particleID)), (int(8*scale), int(8*scale)))
            return self.sprites['particles'][particleID]
        except:
            return self.sprites['error']

    def get_itemSprite(self, itemID, scale=2):
        try:
            if itemID not in self.sprites['items'].keys():
                self.sprites['items'][itemID] = pytransform.scale(pyimage.load('./sprites/items/{}.png'.format(itemID)), (int(16*scale), int(16*scale)))
            return self.sprites['items'][itemID]
        except:
            return self.sprites['error']

    def get_tileEntitySprite(self, tileEntityID):
        #try:
            if tileEntityID not in self.sprites['tile_entities'].keys():
                img = pyimage.load('./sprites/tile_entities/{}.png'.format(tileEntityID))
                dims = (img.get_width(), img.get_height())
                scale = self.tileSize/32
                self.sprites['tile_entities'][tileEntityID] = pytransform.scale(pyimage.load('./sprites/tile_entities/{}.png'.format(tileEntityID)), (int(dims[0]*scale), int(dims[1]*scale)))
            return self.sprites['tile_entities'][tileEntityID]
        #except:
        #    return self.sprites['error']

    def get_tileSprite(self, tileID, adjacent_tiles):
        try:
            if tileID not in self.sprites['tiles'].keys():
                self.sprites['tiles'][tileID] = {}
            if adjacent_tiles not in self.sprites['tiles'][tileID].keys():
                self.sprites['tiles'][tileID][adjacent_tiles] = pytransform.scale(pyimage.load('./sprites/tiles/{}/{}.png'.format(tileID, adjacent_tiles)), (self.tileSize, self.tileSize))
        
            return self.sprites['tiles'][tileID][adjacent_tiles]
        except:
            return self.sprites['error']
    
    def get_propSprite(self, propID):
        try:
            if propID not in self.sprites['props'].keys():
                self.sprites['props'][propID] = pytransform.scale(pyimage.load('./sprites/props/{}.png'.format(propID)), (self.tileSize, self.tileSize))
            return self.sprites['props'][propID]
        except:
            return self.sprites['error']
    
    def get_entitySprites(self, entityID, firstFrameID, lastFrameID):
        scale = 1.5
        dims = {'player':(30,48),'blue_slime':(40,44),'pink_slime':(40,44)}
        assert entityID in dims.keys(), 'Entity dimensions not found'
        # ----- #
        try:
            if entityID not in self.sprites['entities'].keys():
                self.sprites['entities'][entityID]={}
            for i in range(firstFrameID, lastFrameID+1):
                self.sprites['entities'][entityID][i] = pytransform.scale(pyimage.load('./sprites/entities/{}/{}.png'.format(entityID, str(i))), (int(dims[entityID][0]*scale),int(dims[entityID][1]*scale)))
        
            return [self.sprites['entities'][entityID][i] for i in range(firstFrameID, lastFrameID+1)]
        except:
            return self.sprites['error']

    def reset(self, sprites):
        if sprites == 'tiles':
            spriteManager.sprites['tiles'] = {'sand':{'LEFT_UP_RIGHT_DOWN':pytransform.scale(pyimage.load('./sprites/tiles/sand/LEFT_UP_RIGHT_DOWN.png'), (self.tileSize+(self.tileSize//16)*2, self.tileSize+(self.tileSize//16)*2))}}
            spriteManager.sprites['pops'] = {}
        else:
            self.sprites[sprites] = {}
spriteManager = SpriteManager()