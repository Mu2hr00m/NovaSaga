import math
import time
import pygame
import os
import random
import json,pathlib
from assets.managers import common,entity,sound
from assets.managers import constants
from assets.managers import ai
from assets.managers import menus
from assets.managers import items
from assets.managers import projectile,particle
from assets.managers import level,cutscene
common.Entity,common.DynamicLevelTransition,common.Dust,common.Level,common.Bullet,common.ParticleArea = entity.Entity,entity.DynamicTransitionObject,particle.Dust,level.Level,projectile.Bullet,particle.ParticleArea
pygame.mixer.init()
background_files = os.listdir(os.path.join("assets","backgrounds"))
for i in background_files:
    item = pathlib.Path("assets","backgrounds",i)
    if item.suffix==".png":
            item2 = pathlib.Path("assets","backgrounds",item.stem+".json")
            if item2.exists():
                common.backgrounds.append(level.Background(json.loads(item2.read_text()),pygame.image.load(item.joinpath())))
del background_files
def draw():
    timer = time.perf_counter()
    constants.disp_win.fill((0,0,0)) #comment this out for strange fade effect
    constants.layer_0.fill((0,0,0,0))
    constants.layer_1.fill((0,0,0,0))
    constants.layer_2.fill((0,0,0,0))
    constants.layer_3.fill((0,0,0,0))
    constants.layer_4.fill((0,0,0,0))
    constants.layer_4_a.fill((0,0,0,0))
    constants.layer_5.fill((0,0,0,0))
    common.loaded_level.update_camera()
    background = common.loaded_level.background.get_background(pygame.Rect(common.loaded_level.camera[0],common.loaded_level.camera[1],constants.CAM_WIDTH,constants.CAM_HEIGHT))
    constants.layer_0.blit(background,(common.loaded_level.camera[0],common.loaded_level.camera[1]))
    #constants.layer_0 = pygame.transform.scale(constants.layer_0,constants.layer_1.get_size())
    if common.player.overlay_active:
        constants.layer_5.blit(common.player.editable_overlay,((common.player.x-common.loaded_level.camera[0]-128-(constants.CAM_WIDTH/2))*constants.screen_scale,(common.player.y-common.loaded_level.camera[1]-96-(constants.CAM_HEIGHT/2))*constants.screen_scale))
    for box in common.boxes.items():
        box[1].Draw()
        #box[1].afterdraw()
    constants.layer_1.blit(common.loaded_level.display_texture,(0,0))
    for i in common.entities.items():
        i = i[1]
        if callable(getattr(i,"Draw",None)):
            i.Draw()
        elif type(i)==entity.DynamicTransitionObject:
            pygame.draw.rect(constants.layer_2,(128,128,128),i.rect)
    for i in common.particles.items():
        i = i[1]
        i.Draw()
    common.player.Draw()
    if common.active_text!=None:
        common.active_text.update()
    constants.layer_0.blit(constants.layer_1,(0,0))
    constants.layer_0.blit(constants.layer_2,(0,0))
    constants.layer_0.blit(constants.layer_3,(0,0))
    constants.layer_0.blit(constants.layer_4,(0,0))
    constants.layer_0.blit(constants.layer_4_a,(0,0))
    constants.disp_win.blit(common.Scale(common.loaded_level.camera_surface),(0,0))
    constants.layer_5.blit(common.Font("nova",pygame.Rect(0,0,500,16),"sharp fps:  {0} ".format(common.sharp_fps),dest_surface=None),(constants.screen_scale,13*constants.screen_scale))
    constants.layer_5.blit(common.Font("nova",pygame.Rect(0,0,500,16),"smooth fps: {0} ".format(common.fps),dest_surface=None),(constants.screen_scale,18*constants.screen_scale))
    constants.layer_5.blit(common.Font("nova",pygame.Rect(0,0,500,16),"frametime:  {0} ".format(common.frametime_total),dest_surface=None),(constants.screen_scale,23*constants.screen_scale))
    constants.layer_5.blit(common.Font("nova",pygame.Rect(0,0,500,16),"draw ft:    {0} ".format(common.frametime_draw),dest_surface=None),(constants.screen_scale,28*constants.screen_scale))
    constants.disp_win.blit(constants.layer_5,(0,0))
        #common.Font("nova",pygame.Rect((constants.screen_scale,13*constants.screen_scale,8,30)),"fps: "+str(common.tick)+" ")
    pygame.display.update()
    #common.frametime_draw = int((time.perf_counter()-timer)*1000)
    common.frametime_draw_reads[common.frametime_draw_pos.tick] = int((time.perf_counter()-timer)*1000)
    common.frametime_draw = sum(common.frametime_draw_reads)/10
    common.frametime_draw_pos.Loop()
def main():
    common.frametime_draw_pos.Trigger()
    clock = pygame.time.Clock()
    isRunning = True
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                break
            elif event.type == constants.MUSIC_END_EVENT:
                common.loaded_level.play_music()
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
            for i in enumerate(pygame.mouse.get_pressed(5)):
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
            for i in common.entities.items():
                i = i[1]
                if type(i)==entity.Entity:
                    i.AIpointer(i)
                elif type(i)==projectile.Bullet:
                    i.update()
                elif type(i)==entity.DynamicTransitionObject:
                    i.check()
                elif type(i)==entity.TransitionObject:
                    pass
                elif type(i)==particle.ParticleArea:
                    i.spawn_particles()
            for i in common.particles.items():
                i[1].behavior(i[1])
            draw()
            common.entities.update(common.newentities)
            common.particles.update(common.newparticles)
            common.newentities.clear()
            common.newparticles.clear()
            for i in common.delentities:
                del common.entities[i]
            for i in common.delparticles:
                del common.particles[i]
            common.delentities.clear()
            common.delparticles.clear()
        else:
            menus.menu_ticks.Tick()
            if common.menu=="main":
                menus.title()
            elif common.menu=="pause":
                menus.pause()
            elif common.menu=="seed":
                menus.seed()
            elif common.menu=="inventory":
                menus.inventory()
            constants.disp_win.blit(constants.layer_5,(0,0))
            pygame.display.update()
        common.frametime_total = clock.get_rawtime()
        common.fps = clock.get_fps()
        common.sharp_fps = 1000/clock.get_time()
    json.dump(common.Settings,open("settings","w"),indent=4)
    print("game quit no errors")
    pygame.quit()
if __name__ == "__main__":
    main()