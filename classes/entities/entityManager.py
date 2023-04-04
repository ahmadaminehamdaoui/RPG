from random import randint
from classes.maths.vector2 import Vector2
from classes.entities.enemies.blueSlime import BlueSlime
from classes.entities.enemies.pinkSlime import PinkSlime
from classes.spriteManager import spriteManager
from classes.tiles.tilesheet import ts
from classes.devTools import cprint

class EntityManager():
    def __init__(self, map_w, map_h, spawnRate=1, enemyTreshold=25):
        self.map_w = map_w
        self.map_h = map_h
        self.spawnRate = spawnRate
        self.enemyTreshold = enemyTreshold

    def update(self, enemies, camera):
        if len(enemies)<self.enemyTreshold and randint(1,int(400/self.spawnRate)) == 1:
            # DETERMINE SPAWN POINT
            pos = Vector2(0,0)
            if randint(0,2)==0:
                pos.x = camera.pos.x-randint(20,60)
            else:
                pos.x = camera.pos.x+camera.w+randint(0,40)
            if randint(0,2)==0:
                pos.y = camera.pos.y-randint(30,70)
            else:
                pos.y = camera.pos.y+camera.h+randint(0,40)

            if pos.x<0: pos.x=0
            elif pos.x>self.map_w: pos.x=self.map_w
            if pos.y<0: pos.y=0
            elif pos.y>self.map_h: pos.y=self.map_h
  
            # SPAWN ENEMY
            if randint(0,2)==0:
                enemies.append(PinkSlime(pos))
                cprint('Spawned PinkSlime')
            else:
                enemies.append(BlueSlime(pos))
                cprint('Spawned BlueSlilme')
entityManager = EntityManager(ts.get_width()*spriteManager.tileSize, ts.get_height()*spriteManager.tileSize, spawnRate=2)