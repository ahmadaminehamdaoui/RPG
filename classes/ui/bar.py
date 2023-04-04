from turtle import bgcolor
from pygame import draw
from classes.spriteManager import spriteManager

class Bar:
    def __init__(self, pos, dims, bar_color, bg_color, maxValue, value=-1):
        self.pos = pos
        self.width = dims.x
        self.height = dims.y
        # --------- #
        self.bar_color = bar_color
        self.bg_color = bg_color
        # --------- #
        self.maxValue = maxValue
        self.value = value if value!=1 else maxValue
        # --------- #
        # --------- #
        self.bar_left = spriteManager.get_miscSprite('ui/bar_left', xscale=1, yscale=1)
        self.bar_center = spriteManager.get_miscSprite('ui/bar_center', xscale=int(self.width/2), yscale=int(self.height/20))
        self.bar_right = spriteManager.get_miscSprite('ui/bar_right', xscale=1, yscale=1)
    
    def set_value(self, value):
        self.value = value
        if self.value > self.maxValue: self.value=self.maxValue
        elif self.value < 0: self.value=0
    
    def draw(self, screen):
        screen.blit(self.bar_left, (self.pos.x-(self.height/20)*6, self.pos.y-(self.height/20)*6))
        screen.blit(self.bar_center, (self.pos.x, self.pos.y-(self.height/20)*6))
        screen.blit(self.bar_right, (self.pos.x+self.width+(self.height/20)*6-(self.width/450)*8*(450/self.width), self.pos.y-(self.height/20)*6))
        draw.rect(screen, self.bg_color, (self.pos.x, self.pos.y, self.width, self.height))
        draw.rect(screen, self.bar_color, (self.pos.x, self.pos.y, self.value*self.width/self.maxValue, self.height))