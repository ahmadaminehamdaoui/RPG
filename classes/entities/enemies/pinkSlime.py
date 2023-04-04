from classes.maths.vector2 import Vector2
from classes.entities.entity import Entity
from classes.spriteManager import spriteManager
from classes.animatedSprite import AnimatedSprite
from classes.entities.enemies.blueSlime import BlueSlime

class PinkSlime(BlueSlime):
    def __init__(self, pos, vel=Vector2(0,0)):
        super().__init__(pos, vel)
        self.spritesheets = [AnimatedSprite(spriteManager.get_entitySprites('pink_slime', 1, 18), tbf=5)]
        self.speed = 7.5
        self.stat_healthMax = 35
        self.stat_health = self.stat_healthMax
        self.stat_damage = 3

    def update_vel(self, player):
            if self.usedSpritesheet.frameCount >= 4 and self.usedSpritesheet.frameCount <= 9:
                self.vel = (player.pos-self.pos).normalize()
            else:
                self.vel = Vector2(0,0)
    
    def get_type(self):
        return 'Entity.PinkSlime'