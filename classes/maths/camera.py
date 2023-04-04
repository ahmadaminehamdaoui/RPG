import ctypes
from classes.maths.vector2 import Vector2
from classes.spriteManager import spriteManager
user32 = ctypes.windll.user32

class Camera:
    def __init__(self):
        self.pos = Vector2(0,0)
        self.vel = Vector2(0,0)
        self.w, self.h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.w_2 = int(self.w/2)
        self.h_2 = int(self.h/2)
        self.cen = (self.w_2, self.h_2)
        
    def update(self, player, ts):
        self.pos += self.vel
        camera.pos = Vector2(player.pos.x-camera.w_2, player.pos.y-camera.h_2)
        if self.pos.x < 0: self.pos.x = 0
        if self.pos.x+self.w > ts.get_width()*spriteManager.tileSize: self.pos.x=ts.get_width()*spriteManager.tileSize-self.w
        if self.pos.y < 0: self.pos.y = 0
        if self.pos.y+self.h > ts.get_height()*spriteManager.tileSize: self.pos.y=ts.get_height()*spriteManager.tileSize-self.h
camera = Camera()