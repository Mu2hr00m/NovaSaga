import math
import time
import pygame
import os
import random
import json
from assets.managers import common,entity
from assets.managers import constants
from assets.managers import ai
from assets.managers import menus
from assets.managers import items
from assets.managers import projectile
from assets.managers import level,cutscene
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
    common.loaded_level.hud.fill((0,0,0,255))
    common.loaded_level.update_camera()
    for box in common.boxes:
        box.Draw()
    constants.WIN.blit(common.loaded_level.display_texture,(0,0))
    if common.player.overlay_active:
        constants.WIN.blit(common.player.overlay,(common.player.x-(constants.CAM_WIDTH*1.5)-1,common.player.y-(constants.CAM_HEIGHT*1.5)))
    for i in common.enemies:
        if i!=None:
            i.Animation(i)
    for i in common.projectiles:
        if i!=None:
            i.draw()
    for i in common.particles:
        if i!=None:
            i.draw()
    #for box in game_classes.boxes:
        #box.afterdraw()
    for i in common.level_transitions:
        pygame.draw.rect(constants.WIN,(128,128,128),i.rect)
    common.player.Draw()
    if common.active_text!=None:
        common.active_text.update()
    pygame.transform.scale(common.loaded_level.camera_surface,(constants.WIDTH*constants.screen_scale,constants.HEIGHT*constants.screen_scale),constants.disp_win)
    #common.loaded_level.hud.blit(constants.DEF_FONT.render("FPS: "+str(common.tick),False,(128,64,192)),(constants.screen_scale,13*constants.screen_scale))
    common.Font("nova",pygame.Rect((constants.screen_scale,13*constants.screen_scale,8,30)),"fps: "+str(common.tick)+" ")
    constants.disp_win.blit(common.loaded_level.hud,(0,0))
    pygame.display.update()
def main():
    clock = pygame.time.Clock()
    isRunning = True
    tick = 0
    common.run = level.Run()
    common.loaded_level = level.Level()
    common.player = entity.Entity("player","player")
    common.player.texture_size = [4,8]
    common.player.hitbox = pygame.Rect(0,0,8,16)
    common.e=cutscene.TextSequence([cutscene.TextElement("press^kwto jump",common.player,"happy"),90,cutscene.TextElement("\ngo on, press^kw",common.player,"neutral")],1,size=2)
    common.ReloadSettings()
    print("ready")
    while isRunning:
        clock.tick(constants.FPS)
        tick+=1
        if time.time()>common.realclock+1:
            common.tick = tick
            tick = 0
            common.realclock = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                break
        keys = pygame.key.get_pressed()
        for i in common.PressedKeys.keys():
            if type(i)==int:
                common.KeyCooldown[i].Tick()
                if common.KeyCooldown[i].active:
                    common.PressedKeys[i] = False
                else:
                    common.PressedKeys[i] = keys[i]
                if keys[i]:
                    common.KeyCooldown[i].Trigger()
                else:
                    common.KeyCooldown[i].Reset()
        for i in common.PressedKeys.keys():
            if type(i)==int:
                common.PressedKeysNoCooldown[i]=keys[i]
            elif pygame.mouse.get_focused():
                common.PressedKeysNoCooldown[i]=pygame.mouse.get_pressed(5)[int(i[5])-1]
        if pygame.mouse.get_focused():
            for i in enumerate(pygame.mouse.get_pressed()):
                i = ("mouse"+str(i[0]+1),i[1])
                if common.KeyCooldown[i[0]].active:
                    common.KeyCooldown[i[0]].Tick()
                    common.PressedKeys[i[0]] = False
                else:
                    common.PressedKeys[i[0]] = i[1]
                if i[1]:
                    common.KeyCooldown[i[0]].Trigger()
                else:
                    common.KeyCooldown[i[0]].Reset()
        else:
            for i in "12345":
                common.PressedKeys["mouse"+i] = False
        pygame.event.clear()
        if common.menu==None:
            menus.menu_ticks.Trigger()
            common.player.AIpointer(common.player)
            for i in common.enemies:
                if i!=None:
                    i.AIpointer(i)
            for i in common.projectiles:
                if i!=None:
                    i.update()
            for i in common.level_transitions:
                i.check()
            for i in common.particle_spawners:
                i.spawn_particles()
            draw()
        else:
            menus.menu_ticks.Tick()
            if common.menu=="main":
                menus.title()
            elif common.menu=="pause":
                menus.pause()
            elif common.menu=="seed":
                menus.seed()
            constants.disp_win.blit(constants.menu_surface,(0,0))
            pygame.display.update()
    json.dump(common.Settings,open("settings","w"),indent=4)
    print("game quit no errors")
    pygame.quit()
if __name__ == "__main__":
    main()