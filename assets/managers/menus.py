import pygame
import os
from assets.managers import constants,common,level
border_color = (96,0,144)
interior_color = (64,48,80)
ui_path = os.path.join("assets","managers","menu_ui")
title_ui = []
pause_ui = []
menu_ticks = common.Ticker(20)
width_eighth = constants.menu_surface.get_width()/8
height_eighth = constants.menu_surface.get_height()/8
#title_ui.append(pygame.image.load(os.path.join("assets","managers","menu_ui","title_background.png")))
class Button():
    def __init__(self,rect,path,index):
        self.rect = rect
        self.path = path
        self.text = pygame.image.load(os.path.join(constants.ui_path,path))
        self.down_text = self.text.copy()
        border_size = int(constants.screen_scale*1.2)
        for i in range(self.down_text.get_width()):
            for j in range(self.down_text.get_height()):
                if self.down_text.get_at((i,j)) == (0,0x49,0xbf):
                    self.down_text.set_at((i,j),(32,0x92,0xff))
        self.text = pygame.transform.scale(self.text,(self.text.get_width()*constants.screen_scale,constants.BUTTONSIZE-constants.screen_scale*5))
        self.down_text = pygame.transform.scale(self.down_text,(self.down_text.get_width()*constants.screen_scale,constants.BUTTONSIZE-constants.screen_scale*5))
        self.surface = pygame.Surface((self.rect.w,self.rect.h))
        self.down_surface = self.surface.copy()
        pygame.draw.rect(self.surface,(0,0x49,0xbf),pygame.Rect(0,0,self.rect.w,self.rect.h))
        pygame.draw.rect(self.surface,(0,1,0),pygame.Rect(border_size,border_size,self.rect.w-border_size*2,self.rect.h-border_size*2))
        pygame.draw.rect(self.down_surface,(32,0x92,0xff),pygame.Rect(0,0,self.rect.w,self.rect.h))
        pygame.draw.rect(self.down_surface,(64,64,64),pygame.Rect(border_size,border_size,self.rect.w-border_size*2,self.rect.h-border_size*2))
        self.surface.blit(self.text,(self.rect.w/2-self.text.get_width()/2,border_size*2))
        self.down_surface.blit(self.down_text,(self.rect.w/2-self.down_text.get_width()/2,border_size*2))
        self.rect.x = (constants.menu_surface.get_width()/2)-(self.rect.w/2)
        self.rect.y = constants.menu_surface.get_height()/8*(index*0.75+2)
    def Draw(self):
        if pygame.mouse.get_focused():
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                constants.menu_surface.blit(self.down_surface,(self.rect.x,self.rect.y))
            else:
                constants.menu_surface.blit(self.surface,(self.rect.x,self.rect.y))
        else:
            constants.menu_surface.blit(self.surface,(self.rect.x,self.rect.y))

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
title_ui.append(Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"play.png",1))
title_ui.append(Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"settings.png",2))
title_ui.append(Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"quit_from_pause.png",3))
pause_ui.append(ui_background(width_eighth*3,height_eighth*4.5))
pause_ui.append(pygame.transform.scale(pygame.image.load(os.path.join(ui_path,"pause.png")),(150*constants.screen_scale,14*constants.screen_scale)))
pause_ui.append(Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"resumegame.png",0))
pause_ui.append(Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"settings.png",1))
pause_ui.append(Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"restartrun.png",2))
pause_ui.append(Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"quit_to_title.png",3))
pause_ui.append(Button(pygame.Rect(0,0,width_eighth*2,constants.BUTTONSIZE),"quit_from_pause.png",4))
def title():
    global menu_ticks
    constants.menu_surface.fill((0,1,0,0))
    constants.menu_surface.blit(title_ui[0],(width_eighth*2.5,height_eighth*2))
    constants.menu_surface.blit(title_ui[1],(width_eighth*4-title_ui[1].get_width()/2,height_eighth*0.75))
    for element in title_ui:
        if type(element)==Button:
            element.Draw()
    if pygame.mouse.get_focused() and not menu_ticks.active:
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed(5)[0]:
            if title_ui[2].rect.collidepoint(pygame.mouse.get_pos()):
                common.menu = None
                common.run = level.Run(0,os.urandom(16))
                menu_ticks.Trigger()
            elif title_ui[3].rect.collidepoint(pygame.mouse.get_pos()):
                print("settings not implemented")
                menu_ticks.Trigger()
            elif title_ui[4].rect.collidepoint(pygame.mouse.get_pos()):
                print("game quit from main menu")
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        if keys[pygame.K_ESCAPE]:
            common.menu = None
            menu_ticks.Trigger()
def pause():
    global menu_ticks
    constants.menu_surface.fill((0,0,0,255))
    constants.menu_surface.blit(pause_ui[0],(width_eighth*2.5,height_eighth*1.5))
    constants.menu_surface.blit(pause_ui[1],(width_eighth*4-pause_ui[1].get_width()/2,height_eighth*0.5))
    for element in pause_ui:
        if type(element)==Button:
            element.Draw()
    if pygame.mouse.get_focused() and not menu_ticks.active:
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed(5)[0]:
            if pause_ui[2].rect.collidepoint(pygame.mouse.get_pos()):
                common.menu = None
                menu_ticks.Trigger()
            elif pause_ui[3].rect.collidepoint(pygame.mouse.get_pos()):
                print("settings not implemented")
                menu_ticks.Trigger()
            elif pause_ui[4].rect.collidepoint(pygame.mouse.get_pos()):
                common.run = level.Run(0,500)
                common.player.x = constants.DEF_START_POS[0]
                common.player.y = constants.DEF_START_POS[1]
                common.player.x_vel = 0
                common.player.y_vel = 0
                common.menu = None
                menu_ticks.Trigger()
            elif pause_ui[5].rect.collidepoint(pygame.mouse.get_pos()):
                common.menu = "main"
                menu_ticks.Trigger()
            elif pause_ui[6].rect.collidepoint(pygame.mouse.get_pos()):
                print("game quit from pause")
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        if keys[pygame.K_ESCAPE]:
            common.menu = None
            menu_ticks.Trigger()
