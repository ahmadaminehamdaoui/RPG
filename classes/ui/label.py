# MODULES
import pygame
from math import sqrt
from random import randint

fonts = {}
class Label:
    def __init__(self, position, size=13, color=(255,255,255), text='', centered=False):
        self.position = position
        self.size = size
        self.color = color
        self.text = text
        self.centered = centered
    
    def draw(self, surface, text=''):
        if text != '':
            if self.size not in fonts.keys():
                fonts[self.size] = pygame.font.Font('classes/ui/lang/Emulogic.ttf', self.size)
            font = fonts[self.size]
            text = font.render(text, 1, self.color)
            if self.centered:
                surface.blit(text, (self.position.x-text.get_width()/2, self.position.y-text.get_height()/2))
            else:
                surface.blit(text, (self.position.x, self.position.y))