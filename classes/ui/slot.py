from classes.maths.vector2 import Vector2
from classes.spriteManager import spriteManager
from classes.entities.player import player
from classes.inventory.item import Item
from classes.devTools import cprint

class Slot:
    def __init__(self, pos, dims=Vector2(48,48), item=Item('')):
        self.pos = pos
        self.dims = dims
        self.item = item
        self.sprite_idle = spriteManager.get_miscSprite('ui/inventory_slot', xscale=self.dims.x/32, yscale=self.dims.y/32)
        self.sprite_hovered = spriteManager.get_miscSprite('ui/inventory_slot_hovered', xscale=self.dims.x/32, yscale=self.dims.y/32)
        self.sprite_hovered_ol = spriteManager.get_miscSprite('ui/inventory_slot_hovered_overlay', xscale=self.dims.x/32, yscale=self.dims.y/32)
        # --- #
        self.isHovered = False
        #self.isPressed = False
        self.isLocked = False
    
    def update(self, cursor_pos, cursor_state):
        if cursor_pos[0]>self.pos.x and cursor_pos[0]<self.pos.x+self.dims.x and cursor_pos[1]>self.pos.y and cursor_pos[1]<self.pos.y+self.dims.y and not self.isLocked:
            self.isHovered = True
            if cursor_state=='left':
                player.heldItem.update_item(self.item)
                player.selectedItem = self.item
                if (player.vel.x, player.vel.y) == (0,0):
                    if self.item.damage>0:
                        if player.usedSpritesheet != 3: player.set_animation(3)
                    else:
                        if player.usedSpritesheet != 1: player.set_animation(1)
                elif (player.vel.x, player.vel.y) != (0,0):
                    if self.item.damage>0:
                        if player.usedSpritesheet != 2: player.set_animation(2)
                    else:
                        if player.usedSpritesheet != 0: player.set_animation(0)
        else:
            self.isHovered = False
    
    def draw(self, screen):
        if self.isHovered:
            screen.blit(self.sprite_hovered, self.pos.toTuple())
            screen.blit(self.sprite_hovered_ol, (self.pos.x-self.dims.x/32*2, self.pos.y-self.dims.y/32*2))
        else:
            screen.blit(self.sprite_idle, self.pos.toTuple())
        
        if self.item.itemID != '':
            dims = (self.item.sprite.get_width(), self.item.sprite.get_height())
            x = int((self.dims.x-dims[0])/2)
            y = int((self.dims.y-dims[1])/2)
            screen.blit(self.item.sprite, (self.pos.x+x,self.pos.y+y))
