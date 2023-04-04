from random import randint
from classes.maths.vector2 import Vector2
from classes.spriteManager import spriteManager
from classes.projectiles.projectile import Projectile
from classes.particles.particle import Particle

class FireBall(Projectile):
    def __init__(self, pos, vel, stat_damage, stat_knockback, stat_stunTime, isHostile=False):
        super().__init__(pos, vel, stat_damage, stat_knockback, stat_stunTime, isHostile)
        self.sprite = spriteManager.get_miscSprite('projectiles/fire_ball')
        self.width, self.height = self.sprite.get_width(), self.sprite.get_height()
        self.hurtbox = (0,0,int(self.width/2))
    
    def update(self, enemies, player, projectiles, particles):
        self.base_update(enemies, player, projectiles, particles)
        # PARTICLES
        name = 'fire'+str(randint(1,4))
        particles.append(Particle(name, Vector2(self.pos.x,self.pos.y), Vector2(randint(-100,100)/100, randint(-100,100)/100).normalize()*(randint(50,100)/100), lifeTime=randint(20,35)))
    
    def base_kill(self, projectiles, particles):
        for _ in range(10):
            name = 'fire'+str(randint(1,4))
            particles.append(Particle(name, Vector2(self.pos.x+self.width/2,self.pos.y+self.width/2), Vector2(randint(-100,100)/100, randint(-100,100)/100).normalize()*(randint(600,900)/100), lifeTime=randint(40,80)))
        if self in projectiles:
            projectiles.remove(self)

    def draw(self, screen, isDev, camera):
        self.base_draw(screen, isDev, camera)