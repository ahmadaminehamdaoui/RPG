from pygame import mouse
from classes.maths.vector2 import Vector2
from classes.maths.funcs import is_circle_colliding
from classes.maths.camera import camera
from classes.entities.entity import Entity
from classes.projectiles.heldItem import HeldItem
from classes.spriteManager import spriteManager
from classes.animatedSprite import AnimatedSprite
from classes.inventory.item import Item
from classes.projectiles.fireBall import FireBall

class Player(Entity):
    def __init__(self, pos, vel=(0,0)):
        super().__init__(pos, vel)
        # 0 = running, 1 = idle, 2 = running (holding), # 3 = idle (holding)
        self.spritesheets = [AnimatedSprite(spriteManager.get_entitySprites('player', 1, 6)), AnimatedSprite(spriteManager.get_entitySprites('player', 7, 12)),
                        AnimatedSprite(spriteManager.get_entitySprites('player', 13, 18)), AnimatedSprite(spriteManager.get_entitySprites('player', 19, 24))]# TO-DO -> NOUVELLE SPRITESHEET DU JOUEUR PUIS INDIQUER DANS CETTE VARIABLE LES INTERVALLES
        
        self.speed = 8
        self.cbo = (0,50,0,-50) # collision box offset
        self.hitboxes = [[0,0, 20],[0,16, 20]]

        # ---- #
        self.heldItem = HeldItem()
        self.selectedItem = Item('')
        # ---- #
        self.moveVel = Vector2(0,0)

    def update(self, cursor_pos, enemies, particles):
        if not self.dead:
            if self.canMove:
                self.vel = self.moveVel.normalize()
            self.base_update(enemies, particles)
            self.update_animation(cursor_pos)
            self.hurt_check(enemies)
            self.heldItem.update(self, [mouse.get_pos()[0]+camera.pos.x,mouse.get_pos()[1]+camera.pos.y], enemies)

            # ATTACK
            if self.heldItem.attackDelay > 0:
                self.heldItem.attackDelay -= 1
            if self.stat_manaRegenCooldown > 0:
                self.stat_manaRegenCooldown -= 1
            if self.stat_manaRegenCooldown <= 0:
                self.stat_mana += 0.05
            if self.stat_mana > self.stat_manaMax:
                self.stat_mana = self.stat_manaMax
    
    def update_animation(self, cursor_pos):
        if (self.vel.x, self.vel.y) == (0,0) and (self.usedSpritesheet != self.spritesheets[1] and self.usedSpritesheet != self.spritesheets[3]):
            self.set_animation(1) if self.heldItem.stat_damage<=0 else self.set_animation(3)
        elif (self.vel.x, self.vel.y) != (0,0) and (self.usedSpritesheet != self.spritesheets[0] and self.usedSpritesheet != self.spritesheets[2]):
            self.set_animation(0) if self.heldItem.stat_damage<=0 else self.set_animation(2)
        if cursor_pos[0]+camera.pos.x >= self.pos.x:
            self.facingRight = True
        else:
            self.facingRight = False
    
    def attack(self, projectiles, cursor_pos):
        if not self.dead:
            if self.heldItem.attackFrame <= 0 and self.heldItem.attackDelay <= 0:
                self.heldItem.attackFrame = self.heldItem.attackFrameMax
                self.heldItem.stateBottom = not self.heldItem.stateBottom
                self.heldItem.attackDelay = self.heldItem.attackDelayMax
                # ----- #
                if self.selectedItem.projectile != None:
                    if self.stat_mana >= self.selectedItem.manaUse:
                        vel = Vector2((cursor_pos[0]+camera.pos.x)-(self.pos.x+self.width/2), (cursor_pos[1]+camera.pos.y)-(self.pos.y+self.height/2)).normalize()
                        pos = Vector2(self.pos.x+self.width/2, self.pos.y+self.height/2)
                        projectiles.append(FireBall(pos, vel, self.selectedItem.projectileSpeed, self.selectedItem.damage, self.selectedItem.knockback, self.selectedItem.stunTime))
                        self.stat_mana -= self.selectedItem.manaUse
                        self.stat_manaRegenCooldown = self.stat_manaRegenCooldownMax

    def hurt_check(self, enemies):
        if self.stat_vulnerable:
            if self.stunTime <= 0:
                for e in enemies:
                    if not e.dying:
                        for hbx in self.hitboxes:
                            for e_hbx in e.hitboxes:
                                if is_circle_colliding(Vector2(self.pos.x+hbx[0], self.pos.y+hbx[1]), hbx[2], Vector2(e.pos.x+e_hbx[0], e.pos.y+e_hbx[1]), e_hbx[2]):
                                    self.base_hit(1,e.pos,e.stat_knockback,e.stat_stunTime)
                                    break

    def draw(self, screen, isDev):
        if not self.dead:
            self.base_draw(screen, isDev)
            self.heldItem.draw(screen, self, isDev)
    
    def get_type(self):
        return 'Player'       
player = Player(Vector2(48*10,48*10), Vector2(0,0))