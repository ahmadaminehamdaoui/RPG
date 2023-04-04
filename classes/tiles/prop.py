from classes.spriteManager import spriteManager

class Prop:
    def __init__(self, propID):
        self.propID = propID
        self.sprite = spriteManager.get_propSprite(propID)
    
    def __repr__(self):
        return str(self.propID)