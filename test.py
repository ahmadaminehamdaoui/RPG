# ------ TO-DO ------
# https://trello.com/b/Ga28mASW/rpg-game


from ipaddress import v4_int_to_packed
import pygame, sys, ctypes
from random import randint

# --- GAME VARIABLES --- #
sys.setrecursionlimit(10**5)
isDev = False
useQwerty = True
maxFPS = 60

# --- PYGAME INIT --- #
pygame.init()
pygame.display.init()
pygame.display.set_caption('dungeon gen')
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
# pygame.mouse.set_visible(0)

# TESTING
camera_vel = [0,0]
camera_pos = [0,0]

tilemap = [[0 for i in range(50)] for i in range(50)]
size = 20

starting_point = [20,20]
dungeon_len = 10
possible_directions = 'LURD'

# L-U-R-D
def gen_dungeon(chance,directions,dungeon_len,tilemap, pos=starting_point):
    global possible_directions
    # ---- #
    for dir_ in possible_directions:
        if dir_ not in directions:
            if randint(0,int(chance))==0:
                directions += dir_
    print(directions)
    # ---- #
    n_rooms = len(directions) if len(directions)>0 else 1
    next_room_len = dungeon_len//n_rooms

    if next_room_len <= 1: 
        directions = ''
        next_room_len = 0
    # ---- #

    if 'L' in directions:
        gen_dungeon(chance+0.025,'',dungeon_len-1,tilemap,[pos[0]-1, pos[1]])
    if 'U' in directions:
        gen_dungeon(chance+0.025,'',dungeon_len-1,tilemap,[pos[0], pos[1]-1])
    if 'R' in directions:
        gen_dungeon(chance+0.025,'',dungeon_len-1,tilemap,[pos[0]+1, pos[1]])
    if 'D' in directions:
        gen_dungeon(chance+0.025,'',dungeon_len-1,tilemap,[pos[0], pos[1]+1])

    try:
        tilemap[pos[1]][pos[0]]=1
    except: pass
        
gen_dungeon(1,'LRD',15,tilemap)

# --- MAIN GAME LOOP --- #
while True:
    # --- FRAME INIT --- #
    screen.fill((0,0,0))
    currentFPS = round(clock.get_fps(),1)
    cursor_pos = pygame.mouse.get_pos()
     
    # --- INSTANCE UPDATES --- #
    camera_pos[0] += camera_vel[0]
    camera_pos[1] += camera_vel[1]

    # --- INPUT EVENTS --- #
    for event in pygame.event.get():
        ##################################################
        if event.type == pygame.KEYDOWN:
            # -------------------------- #
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_F3:
                isDev = not isDev
            # -------------------------- #
            if event.key == pygame.K_d:
                camera_vel[0] = 5
            if event.key == pygame.K_z:
                camera_vel[1] = -5
            if event.key == pygame.K_q:
                camera_vel[0] = -5
            if event.key == pygame.K_s:
                camera_vel[1] = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                camera_vel[0] = 0
            if event.key == pygame.K_z:
                camera_vel[1] = 0
            if event.key == pygame.K_q:
                camera_vel[0] = 0
            if event.key == pygame.K_s:
                camera_vel[1] = 0

    # --- DRAWING --- #
    for y in range(len(tilemap)):
        for x in range(len(tilemap[0])):
            if tilemap[y][x]==1:
                pygame.draw.rect(screen, (255,255,255), (camera_pos[0]+x*size+x*10, camera_pos[1]+y*size+y*10, size, size))
    # --- #
    pygame.display.update()
    clock.tick(maxFPS)