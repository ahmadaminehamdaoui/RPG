from pygame import draw
from classes.maths.funcs import is_circle_colliding, is_colliding, get_tile_position
from classes.maths.vector2 import Vector2
from classes.maths.customDrawing import relative_blit
from classes.spriteManager import spriteManager
from classes.tiles.tilesheet import ts
from classes.devTools import cprint

class Projectile:
    def __init__(self, pos, vel, speed, stat_damage, stat_knockback, stat_stunTime, isHostile=False, lifeTime=240):
        self.pos = pos
        self.vel = vel
        self.speed = speed
        self.lifeTime = lifeTime
        # --- #
        self.sprite = ''
        self.width, self.height = (self.sprite.get_width(), self.sprite.get_height()) if self.sprite != '' else (0,0)
        # --- #
        self.isHostile = isHostile
        self.hurtbox = (0,0,int(self.width/2))
        self.cbo = [0,0,0,0]
        self.piercing = 1
        # --- #
        self.stat_damage = stat_damage
        self.stat_knockback = stat_knockback
        self.stat_stunTime = stat_stunTime

    def base_update(self, enemies, player, projectiles, particles):
        self.base_update_pos(projectiles, particles)
        self.check_collision(enemies, player)

        # DYING CONDITIONS
        self.lifeTime -= 1
        if self.piercing <= 0 or self.lifeTime <= 0:
            self.base_kill(projectiles, particles)

    def base_update_pos(self, projectiles, particles):
        self.pos += self.vel*self.speed
        # --------------------------- #
        for y in range(-3,3):
            for x in range(-3,3):
                tile_pos = get_tile_position(Vector2(self.pos.x+x*spriteManager.tileSize, self.pos.y+y*spriteManager.tileSize))
                abs_tile_pos = Vector2(tile_pos.x*48, tile_pos.y*48)
                if ts.get_tileID(tile_pos.x, tile_pos.y)=='mountain':
                    if is_colliding(Vector2(self.pos.x+self.cbo[0], self.pos.y+self.cbo[1]), self.width+self.cbo[2], self.height+self.cbo[3], abs_tile_pos, spriteManager.tileSize, spriteManager.tileSize):
                        while is_colliding(Vector2(self.pos.x+self.cbo[0], self.pos.y+self.cbo[1]), self.width+self.cbo[2], self.height+self.cbo[3], abs_tile_pos, spriteManager.tileSize, spriteManager.tileSize):
                            self.pos -= self.vel
                            if (self.vel.x, self.vel.y) == (0,0):
                                break
                        self.base_kill(projectiles, particles)

    def check_collision(self, enemies, player):
        if self.isHostile:
            for hitbox in player.hitboxes:
                if is_circle_colliding(Vector2(self.pos.x+self.hurtbox[0], self.pos.y+self.hurtbox[1]), self.hurtbox[2], Vector2(player.pos.x+player.width/2+hitbox[0], player.pos.y+player.height/2+hitbox[1]), hitbox[2]):
                    player.hit(s_damage=self.stat_damage, s_pos=Vector2(self.pos.x+self.hurtbox[0],self.pos.y+self.hurtbox[1]), s_knockback=self.stat_knockback, s_stunTime=self.stat_stunTime)
                    break
        else:
            for e in enemies:
                for hitbox in e.hitboxes:
                    if is_circle_colliding(Vector2(self.pos.x+self.hurtbox[0], self.pos.y+self.hurtbox[1]), self.hurtbox[2], Vector2(e.pos.x+e.width/2+hitbox[0], e.pos.y+e.height/2+hitbox[1]), hitbox[2]):
                        e.hit(s_damage=self.stat_damage, s_pos=Vector2(self.pos.x+self.hurtbox[0],self.pos.y+self.hurtbox[1]), s_knockback=self.stat_knockback, s_stunTime=self.stat_stunTime)
                        self.piercing -= 1
                        break

    def base_kill(self, projectiles, particles):
        if self in projectiles:
            projectiles.remove(self)

    def base_draw(self, screen, isDev, camera):
        if self.sprite != '':
            relative_blit(self.sprite, self.pos, screen)
        if isDev:
            draw.circle(screen, (0,0,255), (int((self.pos.x+self.width/2)+self.hurtbox[0]-camera.pos.x), int((self.pos.y+self.height/2)+self.hurtbox[1]-camera.pos.y)), self.hurtbox[2], 1)
