from pygame import transform as pytransform
from random import randint
from classes.maths.vector2 import Vector2
from classes.maths.customDrawing import relative_blit
from classes.spriteManager import spriteManager

class Particle:
    def __init__(self, particleID, pos, vel, lifeTime=10, decrease=['product',0.85], scale=(1,3)):  
        self.pos = pos
        self.vel = vel
        self.lifeTime = lifeTime
        self.life = lifeTime
        self.decrease = decrease # describes how the particle's velocity is updated over time
        # ----- #
        self.original_scale = randint(scale[0]*100, scale[1]*100)/100
        self.scale = self.original_scale
        self.sprite = pytransform.scale(spriteManager.get_particleSprite(particleID), (int(8*self.scale), int(8*self.scale))).copy()
        self.image = self.sprite
        self.rotateClockwise = randint(0,1)
        self.rotationSpeed = randint(1,30)
        self.angle = randint(0,360)

    def update(self, particles):
        # MOVEMENT
        self.pos += self.vel
        if self.decrease[0] == 'product': self.vel *= self.decrease[1]
        elif self.decrease[0] == 'add': self.vel += self.decrease[1]
        self.angle += -self.rotationSpeed if self.rotateClockwise else self.rotationSpeed
        if self.angle > 360:
            self.angle = self.angle-360
        elif self.angle < 0:
            self.angle = 360+self.angle
        
        # LIFETIME
        self.life -= 1
        if self.life < 0: particles.remove(self)

        # SPRITE
        if self.life >= 0:
            self.scale = self.original_scale*(self.life/self.lifeTime)
            self.image = pytransform.scale(self.sprite, (int(8*self.scale), int(8*self.scale)))
    
    def draw(self, screen):
        relative_blit(self.image, self.pos, screen)

        