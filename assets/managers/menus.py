import pygame
import os
from assets.managers import game_classes
from assets.managers import constants
border_color = (96,0,144)
interior_color = (64,48,80)
ui_path = os.path.join("assets","managers","menu_ui")
title_ui = []
pause_ui = []
menu_ticks = game_classes.Ticker(20)
width_eighth = constants.menu_surface.get_width()/8
height_eighth = constants.menu_surface.get_height()/8
#title_ui.append(pygame.image.load(os.path.join("assets","managers","menu_ui","title_background.png")))
def ui_background(w,h,transparent=True):
    corner = 10*constants.screen_scale
    surface = pygame.Surface((w,h))
    border_size = int(constants.screen_scale*1.2)
    half_border = int(border_size/2)
    if not transparent:
        surface.fill((0,1,0))
    pygame.draw.rect(surface,interior_color,pygame.Rect(0,corner,w,h-corner*2))
    pygame.draw.rect(surface,interior_color,pygame.Rect(corner,0,w-corner*2,h))
    pygame.draw.circle(surface,interior_color,(corner,corner),corner)
    pygame.draw.circle(surface,interior_color,(corner,h-corner),corner)
    pygame.draw.circle(surface,interior_color,(w-corner,corner),corner)
    pygame.draw.circle(surface,interior_color,(w-corner,h-corner),corner)
    pygame.draw.circle(surface,border_color,(corner,corner),corner,border_size,False,True,False,False)
    pygame.draw.circle(surface,border_color,(corner,h-corner),corner,border_size,False,False,True,False)
    pygame.draw.circle(surface,border_color,(w-corner,corner),corner,border_size,True,False,False,False)
    pygame.draw.circle(surface,border_color,(w-corner,h-corner),corner,border_size,False,False,False,True)
    pygame.draw.line(surface,border_color,(half_border,corner),(half_border,h-corner),border_size)
    pygame.draw.line(surface,border_color,(w-half_border,corner),(w-half_border,h-corner),border_size)
    pygame.draw.line(surface,border_color,(corner,half_border),(w-corner,half_border),border_size)
    pygame.draw.line(surface,border_color,(corner,h-half_border),(w-corner,h-half_border),border_size)
    return surface
title_ui.append(ui_background(width_eighth*3,height_eighth*4,False))
title_ui.append(pygame.transform.scale(pygame.image.load(os.path.join(ui_path,"title.png")),(150*constants.screen_scale,14*constants.screen_scale)))
title_ui.append(game_classes.Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"play.png",1))
title_ui.append(game_classes.Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"settings.png",2))
title_ui.append(game_classes.Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"quit_from_pause.png",3))
pause_ui.append(ui_background(width_eighth*3,height_eighth*4.5))
pause_ui.append(pygame.transform.scale(pygame.image.load(os.path.join(ui_path,"pause.png")),(150*constants.screen_scale,14*constants.screen_scale)))
pause_ui.append(game_classes.Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"resumegame.png",0))
pause_ui.append(game_classes.Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"settings.png",1))
pause_ui.append(game_classes.Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"restartrun.png",2))
pause_ui.append(game_classes.Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"quit_to_title.png",3))
pause_ui.append(game_classes.Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"quit_from_pause.png",4))
def title():
    global menu_ticks
    constants.menu_surface.fill((0,1,0,0))
    constants.menu_surface.blit(title_ui[0],(width_eighth*2.5,height_eighth*2))
    constants.menu_surface.blit(title_ui[1],(width_eighth*4-title_ui[1].get_width()/2,height_eighth*0.75))
    for element in title_ui:
        if type(element)==game_classes.Button:
            element.Draw()
    if pygame.mouse.get_focused() and not menu_ticks.active:
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed(5)[0]:
            if title_ui[2].rect.collidepoint(pygame.mouse.get_pos()):
                constants.menu = None
                menu_ticks.Trigger()
            elif title_ui[3].rect.collidepoint(pygame.mouse.get_pos()):
                print("settings not implemented")
                menu_ticks.Trigger()
            elif title_ui[4].rect.collidepoint(pygame.mouse.get_pos()):
                print("game quit from main menu")
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        if keys[pygame.K_ESCAPE]:
            constants.menu = None
            menu_ticks.Trigger()
def pause():
    global menu_ticks
    constants.menu_surface.fill((0,0,0,255))
    constants.menu_surface.blit(pause_ui[0],(width_eighth*2.5,height_eighth*1.5))
    constants.menu_surface.blit(pause_ui[1],(width_eighth*4-pause_ui[1].get_width()/2,height_eighth*0.5))
    for element in pause_ui:
        if type(element)==game_classes.Button:
            element.Draw()
    if pygame.mouse.get_focused() and not menu_ticks.active:
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed(5)[0]:
            if pause_ui[2].rect.collidepoint(pygame.mouse.get_pos()):
                constants.menu = None
                menu_ticks.Trigger()
            elif pause_ui[3].rect.collidepoint(pygame.mouse.get_pos()):
                print("settings not implemented")
                menu_ticks.Trigger()
            elif pause_ui[4].rect.collidepoint(pygame.mouse.get_pos()):
                game_classes.level.load("test")
                game_classes.player.x = constants.DEF_START_POS[0]
                game_classes.player.y = constants.DEF_START_POS[1]
                game_classes.player.x_vel = 0
                game_classes.player.y_vel = 0
                constants.menu = None
                menu_ticks.Trigger()
            elif pause_ui[5].rect.collidepoint(pygame.mouse.get_pos()):
                constants.menu = "main"
                menu_ticks.Trigger()
            elif pause_ui[6].rect.collidepoint(pygame.mouse.get_pos()):
                print("game quit from pause")
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        if keys[pygame.K_ESCAPE]:
            constants.menu = None
            menu_ticks.Trigger()
