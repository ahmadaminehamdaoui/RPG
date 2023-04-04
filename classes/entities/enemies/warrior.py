from random import randint
from pygame import mouse
from classes.maths.vector2 import Vector2
from classes.maths.funcs import is_circle_colliding
from classes.maths.camera import camera
from classes.entities.entity import Entity
from classes.projectiles.heldItem import HeldItem
from classes.spriteManager import spriteManager
from classes.animatedSprite import AnimatedSprite
from classes.devTools import cprint
from classes.ui.bar import Bar

class Warrior(Entity):
    def __init__(self, pos, vel=(0,0)):
        super().__init__(pos, vel)
        # 0 = running, 1 = idle, 2 = running (holding), # 3 = idle (holding)
        self.spritesheets = [AnimatedSprite(spriteManager.get_entitySprites('player', 1, 6)), AnimatedSprite(spriteManager.get_entitySprites('player', 7, 12)),
                        AnimatedSprite(spriteManager.get_entitySprites('player', 13, 18)), AnimatedSprite(spriteManager.get_entitySprites('player', 19, 24))]# TO-DO -> NOUVELLE SPRITESHEET DU JOUEUR PUIS INDIQUER DANS CETTE VARIABLE LES INTERVALLES
        
        self.speed = randint(4,6)
        self.cbo = (0,50,0,-50) # collision box offset
        self.hitboxes = [[0,0, 20],[0,16, 20]]

        # ---- #
        self.heldItem = HeldItem()
        self.selectedItem = 'iron_sword'

        self.attackTime = 90
        self.attackTimeMax = 90
        # ---- #

    def update(self, *args): # player, enemies, particles
        player, enemies, particles = args[0], args[1], args[2]
        # --------------- #
        if self.stunTime <= 0:
            self.vel = (player.pos-self.pos).normalize()
        if not self.dead:
            self.base_update(enemies, particles)
            self.update_animation(mouse.get_pos())
            self.heldItem.update(self, [player.pos.x, player.pos.y], enemies)

            # ATTACK
            if self.attackTime > 0:
                self.attackTime -= 1
    
    def update_animation(self, cursor_pos):
        if (self.vel.x, self.vel.y) == (0,0) and (self.usedSpritesheet != self.spritesheets[1] and self.usedSpritesheet != self.spritesheets[3]):
            self.set_animation(1) if self.selectedItem == '' else self.set_animation(3)
        elif (self.vel.x, self.vel.y) != (0,0) and (self.usedSpritesheet != self.spritesheets[0] and self.usedSpritesheet != self.spritesheets[2]):
            self.set_animation(0) if self.selectedItem == '' else self.set_animation(2)
        if cursor_pos[0]+camera.pos.x >= self.pos.x:
            self.facingRight = True
        else:
            self.facingRight = False
    
    def attack(self):
        if not self.dead:
            if self.heldItem.attackFrame <= 0 and self.attackTime <= 0:
                self.heldItem.attackFrame = self.heldItem.attackFrameMax
                self.heldItem.stateBottom = not self.heldItem.stateBottom
                self.attackTime = self.attackTimeMax
    
    def hit(self, s_damage, s_pos, s_knockback, s_stunTime):
        self.base_hit(s_damage, s_pos, s_knockback, s_stunTime)

    def draw(self, screen, isDev):
        if not self.dead:
            self.base_draw(screen, isDev)
            self.heldItem.draw(screen, self, isDev)
    
    def get_type(self):
        return 'Entity.Warrior'       