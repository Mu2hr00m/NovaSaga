import math
import time
import pygame
import os
import random
from assets.managers import game_classes
from assets.managers import constants
from assets.managers import ai
from assets.managers import menus
from assets.managers import items
from assets.managers import projectile
def load_level(name="test"):
    game_classes.Level.load(name)
game_classes.player.texture_size = [4,8]
game_classes.player.hitbox = pygame.Rect(0,0,8,16)
game_classes.player.x = constants.DEF_START_POS[0]
game_classes.player.y = constants.DEF_START_POS[1]
game_classes.player.AIpointer = ai.playerAI
game_classes.player.overlay_active = True
def abs(num):
    if num<0:
        num *= -1
    return num
def align_to_grid(pos):
    pos[0] = int(pos[0]/constants.BLOCK_SIZE)*constants.BLOCK_SIZE
    pos[1] = int(pos[1]/constants.BLOCK_SIZE)*constants.BLOCK_SIZE
    return pos
def draw():
    constants.WIN.fill((48,48,48))
    game_classes.level.hud.fill((0,0,0,255))
    game_classes.level.update_camera()
    for i in game_classes.enemies:
        if i!=None:
            i.Animation(i)
    for i in projectile.projectiles:
        if i!=None:
            i.draw()
    if game_classes.player.overlay_active:
        constants.WIN.blit(game_classes.player.overlay,(game_classes.player.x-(constants.CAM_WIDTH*1.5),game_classes.player.y-(constants.CAM_HEIGHT*1.5)))
    for box in game_classes.boxes:
        box.Draw()
    constants.WIN.blit(game_classes.level.display_texture, (0,0))
    #for box in game_classes.boxes:
        #box.afterdraw()
    for i in game_classes.level_transitions:
        pygame.draw.rect(constants.WIN,(128,128,128),i.rect)
    game_classes.player.Draw()
    pygame.transform.scale(game_classes.level.camera_surface,(constants.WIDTH*constants.screen_scale,constants.HEIGHT*constants.screen_scale),constants.disp_win)
    game_classes.level.hud.blit(constants.DEF_FONT.render("FPS: "+str(constants.tick),False,(128,64,192)),(constants.screen_scale,13*constants.screen_scale))
    constants.disp_win.blit(game_classes.level.hud,(0,0))
    pygame.display.update()
def main():
    clock = pygame.time.Clock()
    isRunning = True
    tick = 0
    print("ready")
    while isRunning:
        clock.tick(constants.FPS)
        tick+=1
        if time.time()>constants.realclock+1:
            constants.tick = tick
            tick = 0
            constants.realclock = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                break
        pygame.event.clear()
        if constants.menu==None:
            menus.menu_ticks.Trigger()
            game_classes.player.AIpointer(game_classes.player)
            for i in game_classes.enemies:
                if i!=None:
                    i.AIpointer(i)
            for i in projectile.projectiles:
                if i!=None:
                    i.update()
            for i in game_classes.level_transitions:
                i.check()
            draw()
        else:
            menus.menu_ticks.Tick()
            if constants.menu=="main":
                menus.title()
            elif constants.menu=="pause":
                menus.pause()
            constants.disp_win.blit(constants.menu_surface,(0,0))
            pygame.display.update()
    print("game quit no errors")
    pygame.quit()
if __name__ == "__main__":
    main()