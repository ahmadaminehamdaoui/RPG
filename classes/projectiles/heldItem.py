import pygame
from classes.spriteManager import spriteManager
from classes.maths.vector2 import Vector2
from classes.maths.camera import camera
from classes.maths.customDrawing import relative_blit
from classes.maths.funcs import is_circle_colliding
from classes.devTools import cprint

class HeldItem:
    def __init__(self, pos= Vector2(24,24), attackFrameMax=10):
        self.pos = pos
        #
        self.offset = Vector2(20,0)
        self.sprite = spriteManager.get_itemSprite('held_iron_sword')
        self.rect = self.sprite.get_rect()
        self.image = self.sprite
        # ----------------- #
        self.slash_pos = self.pos
        #
        self.slash_offset = Vector2(60,0)
        self.slash_sprite1 = spriteManager.get_itemSprite('slash_1', scale=4)
        self.slash_sprite2 = spriteManager.get_itemSprite('slash_2', scale=4)
        self.slash_used_sprite = self.slash_sprite1
        self.slash_image = None
        self.slash_rect = self.slash_sprite1.get_rect()
        # ----------------- #
        self.attackFrame = 0
        self.attackFrameMax = attackFrameMax
        self.stateBottom = False

        # ----------------- #
        self.hurtboxes = [[0,0], 40]
        self.hurtboxCenterPoint = Vector2(0,0)

        # --------------------------- #
        self.stat_damage = 7
        self.stat_stunTime = 30
        self.stat_knockback = 2.5
        self.attackDelayMax = 15
        self.attackDelay = self.attackDelayMax

    def update(self, owner, pointer, enemies):
        self.update_pos(owner, pointer)
        self.rotate(owner, pointer)
        self.check_collision(owner, pointer, enemies)
        self.update_slash_effect(owner, pointer)
        self.rotate_slash_effect(owner, pointer)

    def check_collision(self, owner, pointer, enemies):
        if self.stat_damage > 0:
            angle = pygame.Vector2(pointer[0] - owner.pos.x+int(owner.width/2), pointer[1] - owner.pos.y-int(owner.height/2)).as_polar()[1]
            slash_offset = Vector2(self.slash_offset.x+self.hurtboxes[0][0], self.slash_offset.y+self.hurtboxes[0][1])
            new_offset = slash_offset.rotateBy(angle)
            self.hurtboxCenterPoint = Vector2(owner.pos.x+owner.width/2+new_offset.x, owner.pos.y+owner.height/2+new_offset.y)
            if self.attackFrame == self.attackFrameMax-1:
                for e in enemies:
                    for hitbox in e.hitboxes:
                        try:
                            if is_circle_colliding(self.hurtboxCenterPoint, self.hurtboxes[1], Vector2(e.pos.x+e.width/2+hitbox[0], e.pos.y+e.height/2+hitbox[1]), hitbox[2]):
                                e.hit(s_damage=self.stat_damage, s_pos=owner.pos, s_knockback=self.stat_knockback, s_stunTime=self.stat_stunTime)
                                break
                        except:
                            cprint('collision error')

    def update_pos(self, owner, pointer):
        # --- DEFINE POS ON CIRCLE AROUND THE owner --- #
        angle = pygame.Vector2(pointer[0] - owner.pos.x+int(owner.width/2), pointer[1] - owner.pos.y-int(owner.height/2)).as_polar()[1]
        if angle <= 90 and angle > -90:
            angle -= 90 if self.stateBottom <= 0 else 180
        else:
            angle += 90 if self.stateBottom <= 0 else 0
        # --
        if self.stateBottom:
            angle += 270
        # --
        new_offset = self.offset.rotateBy(angle)
        self.pos = Vector2(new_offset.x, new_offset.y)
        #  --------------------------------------------------- #

    def rotate(self, owner, pointer):
        # --- ROTATION OF THE SPRITE --- #
        angle = pygame.Vector2(pointer[0] - owner.pos.x+int(owner.width/2), pointer[1] - owner.pos.y-int(owner.height/2)).as_polar()[1]
        if angle <= 90 and angle > -90:
            if self.attackFrame <= 0:
                # IMAGE WHEN NOT ATTACKING
                self.image = pygame.transform.rotate(self.sprite, -angle+135)
            else:
                if self.stateBottom:
                    # IMAGE WHEN ATTACKING (FROM BOTTOM)
                    self.image = pygame.transform.rotate(self.sprite, -angle+135+(self.attackFrame)*(180/self.attackFrameMax))
                else:
                    # IMAGE WHEN ATTACK (FROM TOP)
                    self.image = pygame.transform.rotate(self.sprite, -angle+135-(self.attackFrame)*(180/self.attackFrameMax))
        else:
            if self.attackFrame <= 0:
                # IMAGE WHEN NOT ATTACKING
                self.image = pygame.transform.flip(pygame.transform.rotate(self.sprite, angle-45), True, False)
            else:
                if self.stateBottom:
                    # IMAGE WHEN ATTACKING (FROM BOTTOM)
                    self.image = pygame.transform.flip(pygame.transform.rotate(self.sprite, angle-45+(self.attackFrame)*(180/self.attackFrameMax)), True, False)
                else:
                    # IMAGE WHEN ATTACK (FROM TOP)
                    self.image = pygame.transform.flip(pygame.transform.rotate(self.sprite, angle-45-(self.attackFrame)*(180/self.attackFrameMax)), True, False)
        self.rect = self.image.get_rect(center=self.rect.center)

        # ------------------------------ #
        if self.attackFrame > 0:
            self.attackFrame -= 1

    def update_slash_effect(self, owner, pointer):
        # -- DEFINE SLASH POS ON CIRCLE -- #
        slash_angle = pygame.Vector2(pointer[0] - owner.pos.x+int(owner.width/2), pointer[1] - owner.pos.y-int(owner.height/2)).as_polar()[1]
        slash_offset = self.slash_offset.rotateBy(slash_angle)
        self.slash_pos = Vector2(slash_offset.x, slash_offset.y)

        # -- DEFINE SLASH IMAGE -- #
        if self.attackFrame >= int(self.attackFrameMax/2):
            self.slash_used_sprite = self.slash_sprite1
        elif self.attackFrame > 0:
            self.slash_used_sprite = self.slash_sprite2
        else:
            self.slash_used_sprite = None

    def rotate_slash_effect(self, owner, pointer):
        if self.slash_used_sprite != None:
            angle = pygame.Vector2(pointer[0] - owner.pos.x+int(owner.width/2), pointer[1] - owner.pos.y-int(owner.height/2)).as_polar()[1]
            if angle <= 90 and angle > -90:
                if self.stateBottom:
                    self.slash_image = pygame.transform.rotate(self.slash_used_sprite, -angle)
                else:
                    self.slash_image = pygame.transform.flip(pygame.transform.rotate(self.slash_used_sprite, angle), False, True)
            else:
                if self.stateBottom:
                    self.slash_image = pygame.transform.flip(pygame.transform.rotate(self.slash_used_sprite, angle), False, True)
                else:
                    self.slash_image = pygame.transform.rotate(self.slash_used_sprite, -angle)
            self.slash_rect = self.slash_image.get_rect(center=self.slash_rect.center)

    def update_item(self, item):
        self.sprite = spriteManager.get_miscSprite('items/held_'+item.itemID, xscale=2.5, yscale=2.5)
        self.stat_damage = item.damage
        self.stat_stunTime = item.stunTime
        self.stat_knockback = item.knockback
        self.attackDelayMax = item.useTime
        self.attackDelay = item.useTime

    def draw(self, screen, owner, isDev):
        if self.stat_damage > 0:
            # DRAWING SLASH EFFECT
            if self.slash_image != None and self.slash_used_sprite != None:
                relative_blit(self.slash_image,Vector2(owner.pos.x+self.slash_pos.x+self.slash_rect.topleft[0],owner.pos.y+10+self.slash_pos.y+self.slash_rect.topleft[1]),screen)
            # DRAWING ITEM
            if self.image != None:
                relative_blit(self.image,Vector2(owner.pos.x+self.pos.x+self.rect.topleft[0],owner.pos.y+10+self.pos.y+self.rect.topleft[1]),screen)
            if isDev:
                pos = self.hurtboxCenterPoint
                pygame.draw.circle(screen, (0,255,0), (int(pos.x-camera.pos.x), int(pos.y-camera.pos.y)), self.hurtboxes[1], 1)
