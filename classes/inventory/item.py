from pygame import Surface
from classes.spriteManager import spriteManager
from classes.projectiles.fireBall import FireBall

class Item:
    def __init__(self, itemID=''):
        self.itemID = itemID
        self.sprite = spriteManager.get_itemSprite(itemID, scale=2)
        
        if self.itemID=='iron_sword':
            self.useTime = 15
            self.damage = 7
            self.knockback = 2.5
            self.stunTime = 30
            # --- #
            self.manaUse = 0
            self.projectile = None
            self.projectileSpeed = 0
        elif self.itemID=='fire_staff':
            self.useTime = 15
            self.damage = 3
            self.knockback = 1
            self.stunTime = 25
            # --- #
            self.manaUse = 1
            self.projectile = 'FireBall'
            self.projectileSpeed = 16
        else:
            self.useTime = 0
            self.damage = 0
            self.knockback = 0
            self.stunTime = 0
            # --- #
            self.manaUse = 0
            self.projectile = None
            self.projectileSpeed = 0
    
    def is_weapon(self):
        return True if self.damage>0 else False