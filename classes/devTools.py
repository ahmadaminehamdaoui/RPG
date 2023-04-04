import pygame
from classes.ui.label import Label
from classes.maths.funcs import get_tile_position
from classes.maths.vector2 import Vector2
from classes.maths.camera import camera
from classes.tiles.tilesheet import ts

class Console:
    def __init__(self, pos=Vector2(0, camera.h)):
        self.pos = pos
        self.content = ['' for i in range(30)]
        self.labels = [Label(Vector2(10,self.pos.y-(i+3)*12), size=12) for i in range(30)]
        # TEXT ENTRY
        self.entry_text = ''
        self.entry_label = Label(Vector2(10,self.pos.y-20), size=12)
        self.isWriting = False
    
    def print(self, text):
        self.content.insert(0,str(text))
            
    def draw(self, screen):
        self.entry_label.text = '>'+self.entry_text if self.isWriting else self.entry_text
        self.entry_label.draw(screen, self.entry_label.text)
        for i in range(len(self.labels)):
            self.labels[i].text = self.content[i]
            self.labels[i].draw(screen, self.labels[i].text)
console = Console()

def cprint(text):
    console.print(text)

# ------------------- #
labels = [Label(Vector2(10,i*13)) for i in range(50)]
def draw_dev_UI(screen, isDev, currentFPS, player, enemies, camera):
    if isDev:
        # ----- LABELS ----- #
        texts = ['fps.... '+str(currentFPS), 

        'pos.... '+str(get_tile_position(player.pos)).replace('Vector2', 'vec2'),
        'tile... '+str(ts.get_tileID(int(player.pos.x//48),int((player.pos.y+player.height)//48))),
        'prop... '+str(ts.get_propID(int(player.pos.x//48),int((player.pos.y+player.height)//48))),

        'rot_vec '+str(Vector2(round(pygame.mouse.get_pos()[0] - player.pos.x-camera.pos.x,5), round(pygame.mouse.get_pos()[1] - player.pos.y-camera.pos.y,5))).replace('Vector2', 'vec2'),
        'atk_frm '+str(player.heldItem.attackFrame)]
        
        for i in range(len(texts)):
            labels[i].text = texts[i]
            labels[i].draw(screen, labels[i].text)
        
        for e in enemies:
            pygame.draw.line(screen, (255,0,255), (player.pos.x-camera.pos.x, player.pos.y-camera.pos.y), (e.pos.x-camera.pos.x, e.pos.y-camera.pos.y))

        # ----- CONSOLE ----- #
        console.labels[0].draw(screen)
        console.draw(screen)