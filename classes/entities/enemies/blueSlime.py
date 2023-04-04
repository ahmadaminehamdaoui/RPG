from classes.maths.vector2 import Vector2
from classes.entities.entity import Entity
from classes.spriteManager import spriteManager
from classes.animatedSprite import AnimatedSprite

class BlueSlime(Entity):
    def __init__(self, pos, vel=Vector2(0,0)):
        super().__init__(pos, vel)
        self.spritesheets = [AnimatedSprite(spriteManager.get_entitySprites('blue_slime', 1, 16), tbf=5)]
        self.cbo = (5,50,-10,-50)
        self.hitboxes = [[0,10,20],[-20,20,10],[20,20,10]]
        self.speed = 6
        # --------- #
    
    def update(self, *args): # player, enemies, particles,
        player, enemies, particles = args[0], args[1], args[2]
        # --------------- #
        self.base_update(enemies, particles)
        if self.stunTime > 0:
            if self.dying:
                self.usedSpritesheet.reset()
        else:
            self.update_vel(player)
    
    def update_vel(self, player):
            if self.usedSpritesheet.frameCount >= 4 and self.usedSpritesheet.frameCount <= 7:
                self.vel = (player.pos-self.pos).normalize()
            else:
                self.vel = Vector2(0,0)
    
    def hit(self, s_damage, s_pos, s_knockback, s_stunTime):
        self.base_hit(s_damage, s_pos, s_knockback, s_stunTime)
    
    def draw(self, screen, isDev):
        self.base_draw(screen, isDev)
    
    def get_type(self):
        return 'Entity.BlueSlime'