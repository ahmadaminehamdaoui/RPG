from random import randint
from pygame import transform as pytransform
from pygame import Rect as pyRect
from pygame import draw
from classes.maths.vector2 import Vector2
from classes.maths.customDrawing import relative_blit
from classes.maths.funcs import get_tile_position, is_colliding, color_surface
from classes.maths.camera import camera
from classes.spriteManager import spriteManager
from classes.animatedSprite import AnimatedSprite
from classes.tiles.tilesheet import ts
from classes.devTools import cprint
from classes.particles.particle import Particle

class Entity:
    def __init__(self, pos, vel):
        # movement
        self.pos = pos
        self.oldVel = Vector2(0,0)
        self.vel = vel
        self.speed = 1
        self.canMove = True

        # animations
        self.iniatedSpritesheet = False
        self.spritesheets = None
        self.usedSpritesheet = None
        self.facingRight = True

        # tile collisions
        self.cbo = (0,0,0,0) # collision box offset (tiles)
        self.width = None
        self.height = None

        # entity collisions
        self.hitboxes = [[0,0,20]] # hitboxes

        self.hitCounterMax = 10
        self.hitCounter = 0
        self.hitVel = Vector2(0,0)
        self.stunTime = 0

        self.dead = False
        self.dying = False
        self.dyingCounter = 0
        self.dyingCounterMax = 2
        self.dyingSpriteWhite = False

        # stats
        self.stat_vulnerable = True
        self.stat_healthMax = 20
        self.stat_health = self.stat_healthMax
        self.stat_manaMax = 10
        self.stat_mana = self.stat_manaMax
        self.stat_manaRegenCooldownMax = 150
        self.stat_manaRegenCooldown = self.stat_manaRegenCooldownMax

        self.stat_damage = 2 #
        self.stat_stunTime = 30 #
        self.stat_knockback = 2.5 #

    def set_animation(self, key):
        self.usedSpritesheet = self.spritesheets[key]
        self.usedSpritesheet.frameCount = 1
        self.usedSpritesheet.fpsCount = 1

    def base_update(self, enemies, particles):
        if not self.iniatedSpritesheet:
            self.usedSpritesheet = self.spritesheets[0]
            # tile collisions
            self.width = int(self.spritesheets[0].get_sprite().get_width())
            self.height = int(self.spritesheets[0].get_sprite().get_height())
            #
            self.iniatedSpritesheet = True
        self.base_update_pos()

        # SPRITESHEET
        self.usedSpritesheet.update()
        if self.vel.x > 0:
            self.facingRight = True
        elif self.vel.x < 0:
            self.facingRight = False

        # HIT ANIMATION
        if self.hitCounter > 0:
            self.hitCounter -= 1
        if self.stunTime > 0:
            self.stunTime -= 1
            if self.dying and self.stunTime == 0:
                self.base_kill(enemies, particles)
        if self.dying and self.dyingCounter >= 0:
            self.dyingCounter -= 1
            if self.dyingCounter < 0:
                self.dyingCounter = self.dyingCounterMax
                self.dyingSpriteWhite = not self.dyingSpriteWhite
        if self.stunTime>0:
            self.canMove = False
        else:
            self.canMove = True

    def base_update_pos(self):
        self.pos += self.vel*self.speed
        # --------------------------- #
        for y in range(-3,3):
            for x in range(-3,3):
                tile_pos = get_tile_position(Vector2(self.pos.x+x*spriteManager.tileSize, self.pos.y+y*spriteManager.tileSize))
                abs_tile_pos = Vector2(tile_pos.x*48, tile_pos.y*48)
                if ts.is_solid(tile_pos.x, tile_pos.y):
                    while is_colliding(Vector2(self.pos.x+self.cbo[0], self.pos.y+self.cbo[1]), self.width+self.cbo[2], self.height+self.cbo[3], abs_tile_pos, spriteManager.tileSize, spriteManager.tileSize):
                        self.pos -= self.vel
                        if (self.vel.x, self.vel.y) == (0,0):
                            self.pos.y += 1

        if self.stunTime > 0:
            self.vel *= 0.9

    def base_hit(self, s_damage, s_pos, s_knockback, s_stunTime):
        if self.stat_vulnerable:
            if not self.dying:
                self.stat_health -= s_damage
                if self.stat_health <= 0:
                    self.stat_health = 0
                    self.dying = True
                    self.dyingCounter = self.dyingCounterMax
                    self.dyingSpriteWhite = True
                    self.vel = (self.pos-s_pos).normalize()*s_knockback*1.5
                    self.stunTime = 40
                # hit post-effects
                else:
                    self.hitCounter = self.hitCounterMax
                    self.vel = (self.pos-s_pos).normalize()*s_knockback
                    self.stunTime = s_stunTime
                    self.canMove = False

    def base_kill(self, enemies, particles):
        self.dead = True
        for _ in range(10):
            particles.append(Particle('circle', Vector2(self.pos.x+self.width/2,self.pos.y+self.width/2), Vector2(randint(-100,100)/100, randint(-100,100)/100).normalize()*(randint(300,600)/100), lifeTime=randint(15,40)))

        if 'Entity' in self.get_type():
            if self in enemies:
                enemies.remove(self)

    def base_draw(self, screen, isDev):
        def draw_(screen, isDev):
            usedSprite = self.usedSpritesheet.get_sprite() if self.facingRight else pytransform.flip(self.usedSpritesheet.get_sprite(), True, False)
            if self.dying:
                usedSprite = color_surface(usedSprite.copy(),(255,255,255)) if self.dyingSpriteWhite else usedSprite
            else:
                usedSprite = usedSprite if self.hitCounter <= 0 else color_surface(usedSprite.copy(),(255,255,255))
            relative_blit(usedSprite, self.pos, screen)

            if isDev:
                for hitbox in self.hitboxes:
                    draw.circle(screen, (0,0,255), (int((self.pos.x+self.width/2)+hitbox[0]-camera.pos.x), int((self.pos.y+self.height/2)+hitbox[1]-camera.pos.y)), hitbox[2], 1)
                draw.rect(screen, (255,0,0), pyRect(self.pos.x+self.cbo[0]-camera.pos.x, self.pos.y+self.cbo[1]-camera.pos.y, self.width+self.cbo[2], self.height+self.cbo[3]), 1)

        if not self.dead:
            try:
                draw_(screen, isDev)
            except: pass

    def get_type(self):
        return 'Entity'