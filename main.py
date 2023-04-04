

import pygame, sys, ctypes
# ------------------- #
from classes.maths.camera import camera
from classes.maths.vector2 import Vector2
from classes.maths.funcs import color_surface
from classes.tiles.tilesheet import ts
from classes.entities.player import player
from classes.entities.entityManager import entityManager
from classes.ui.canvas import draw_gameCanvas
from classes.ui.slot import Slot
from classes.inventory.item import Item
from classes.projectiles.fireBall import FireBall
from classes.devTools import draw_dev_UI, cprint, console

# --- GAME SETTINGS --- #
isDev = False
useQwerty = True
maxFPS = 60
currentFPS = 0
preloadColorSurface = False

# --- PYGAME INIT --- #
pygame.init()
pygame.display.init()
pygame.display.set_caption('rpg')
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
# pygame.mouse.set_visible(0)

# --- VARIABLES --- #
# cursor
cursor_state = 'none'
cursor_states = {1:'left',2:'middle',3:'right',4:'scroll_up',5:'scroll_down'}

# ui
slots = [Slot(Vector2(camera.w_2-48*2-6,camera.h-60), item=Item('iron_sword')), Slot(Vector2(camera.w_2-48-2,camera.h-60), item=Item('fire_staff')), Slot(Vector2(camera.w_2+2,camera.h-60)), Slot(Vector2(camera.w_2+48+6,camera.h-60))]
player.heldItem.update_item(slots[0].item)

# lists
rules = []
enemies = []
particles = []
projectiles = [FireBall(Vector2(0,0),Vector2(0.5,0.5),0,0,0)]

# --- MAIN GAME LOOP --- #
while True:
    # --- GAME INIT --- #
    if not preloadColorSurface:
        player.update(pygame.mouse.get_pos(), enemies, particles)
        color_surface(player.usedSpritesheet.get_sprite().copy(),(255,255,255))
        preloadColorSurface = True

    # --- FRAME INIT --- #
    screen.fill((157,118,88))
    currentFPS = round(clock.get_fps(),1)
    cursor_pos = pygame.mouse.get_pos()

    # --- INSTANCE UPDATES --- #
    for s in slots:
        s.update(cursor_pos, cursor_state)
    for e in enemies:
        e.update(player, enemies, particles)
    for p in particles:
        p.update(particles)
    for p in projectiles:
        p.update(enemies, player, projectiles, particles)
    player.update(cursor_pos, enemies, particles)
    camera.update(player, ts)
    entityManager.update(enemies, camera)

    # --- INPUT EVENTS --- #
    for event in pygame.event.get():
        ##################################################
        if event.type == pygame.KEYDOWN:
            # IF WRITING IN THE CONSOLE, DISABLE ALL KEY INPUTS EXCEPT FOR TEXT ENTRY
            if isDev and console.isWriting:
                if event.key == pygame.K_RETURN:
                    args = console.entry_text.split()
                    params = ' '.join(args[1:])
                    ##########
                    if len(args) > 0:
                        if args[0] == 'exec':
                            exec(params)
                            cprint(f'"{params}" executed successfully')
                        elif args[0] == 'rule':
                            params = ' '.join(args[1:-1])
                            if params=='' and args[-1]=='clear':
                                rules = []
                                cprint('The rules have been cleared')
                            else:
                                try:
                                    exec(params)
                                    cprint(f'The rule "{params}" has been created')
                                    rules.append([params, int(args[-1]), 0])
                                except:
                                    cprint(f'The rule "{params}" cannot be created')
                        elif args[0] == 'spawn':
                            name = ''
                            i = 0
                            while i < len(args[1]):
                                if args[1][i] == '_':
                                    name += args[1][i+1].upper()
                                    i+=1
                                else:
                                    name += args[1][i] if i>0 else args[1][i].upper()
                                i+=1
                            if len(args) >= 4:
                                pos = args[3]
                            else:
                                pos = Vector2(0,0)
                            for i in range(int(args[2])):
                                exec(f'enemies.append({name}({pos}))')
                        else:
                            cprint('Unknown command')
                    ##########
                    console.entry_text = ''
                    console.isWriting = False
                elif event.key == pygame.K_BACKSPACE:
                    console.entry_text = console.entry_text[:-1]
                else:
                    console.entry_text += event.unicode
            # KEY INPUT CHECKS WHEN NOT WRITING
            else:
                if isDev and event.key == pygame.K_RETURN:
                    console.isWriting = not console.isWriting
                # -------------------------- #
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_F3:
                    isDev = not isDev
                # -------------------------- #
                elif event.key == pygame.K_d:
                    player.moveVel.x = 1
                elif event.key == pygame.K_s and player.stunTime==0:
                    player.moveVel.y = 1
                if useQwerty:
                    if event.key == pygame.K_w and player.stunTime==0:
                        player.moveVel.y = -1
                    elif event.key == pygame.K_a and player.stunTime==0:
                        player.moveVel.x = -1
                else:
                    if event.key == pygame.K_z and player.stunTime==0:
                        player.moveVel.y = -1
                    elif event.key == pygame.K_q and player.stunTime==0:
                        player.moveVel.x = -1
                # -------------------------- #


        ##################################################
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                if player.moveVel.x>0: player.moveVel.x = 0
            if event.key == pygame.K_s:
                if player.moveVel.y>0: player.moveVel.y = 0
            if useQwerty:
                if event.key == pygame.K_w:
                    if player.moveVel.y<0: player.moveVel.y = 0
                elif event.key == pygame.K_a:
                    if player.moveVel.x<0: player.moveVel.x = 0
            else:
                if event.key == pygame.K_z:
                    if player.moveVel.y<0: player.moveVel.y = 0
                elif event.key == pygame.K_q:
                    if player.moveVel.x<0: player.moveVel.x = 0

        ##################################################
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cursor_state = cursor_states[event.button]
            if cursor_state == 'left':
                player.attack(projectiles, cursor_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            cursor_state = 'none'
        '''
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if cursor.shown: cursor.click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            cursor.click = False
        '''

    # --- RULES --- #
    for rule in rules:
        rule[2] += 1
        if rule[2] >= rule[1]:
            rule[2] = 0
            exec(rule[0])

    # --- DRAWING --- #
    ts.draw(screen)
    player.draw(screen, isDev)
    for e in enemies:
        e.draw(screen, isDev)
    for p in particles:
        p.draw(screen)
    for p in projectiles:
        p.draw(screen, isDev, camera)
    for s in slots:
        s.draw(screen)
    draw_gameCanvas(screen)
    draw_dev_UI(screen, isDev, currentFPS, player, enemies, camera)

    # --- #
    pygame.display.update()
    clock.tick(maxFPS)
