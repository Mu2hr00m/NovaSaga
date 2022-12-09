import pygame
import os,math
from assets.managers import constants,common,level,items
border_color = (96,0,144)
interior_color = (64,48,80)
ui_path = os.path.join("assets","managers","menu_ui")
title_ui = []
pause_ui = []
seed_ui = []
menu_ticks = common.Ticker(20)
width_eighth = constants.menu_surface.get_width()/8
height_eighth = constants.menu_surface.get_height()/8
#title_ui.append(pygame.image.load(os.path.join("assets","managers","menu_ui","title_background.png")))
class Button():
    def __init__(self,rect,path,index=0):
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
    corner = 5*constants.screen_scale
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
title_ui.append(pygame.transform.scale(pygame.image.load(os.path.join(ui_path,"title.png")),(130*constants.screen_scale,18*constants.screen_scale)))
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
for i in "0123456789abcdef":
    seed_ui.append(Button(pygame.Rect(0,0,32*constants.screen_scale,32*constants.screen_scale),"seed_"+i+".png",0))
for i in enumerate(seed_ui):
    i[1].surface = pygame.image.load(os.path.join(ui_path,i[1].path))
    surface2 = i[1].surface.copy()
    arr = pygame.PixelArray(surface2)
    arr.replace((144,128,192),(192,160,255))
    arr.close()
    i[1].down_surface = surface2
    i[1].surface = pygame.transform.scale(i[1].surface,(32*constants.screen_scale,32*constants.screen_scale))
    i[1].down_surface = pygame.transform.scale(i[1].down_surface,(32*constants.screen_scale,32*constants.screen_scale))
    i[1].rect.x = (i[0]%4*34+58)*constants.screen_scale
    i[1].rect.y = (math.floor(i[0]/4)*34+44)*constants.screen_scale
seed_ui.append(ui_background(width_eighth*6,height_eighth*7))
seed_ui.append(pygame.transform.scale(pygame.image.load(os.path.join(ui_path,"seedselect.png")),(58*constants.screen_scale,14*constants.screen_scale)))
seed_ui.append([])
inventory_ui = [ui_background(width_eighth*6,height_eighth*6)]
inventory_ui.append(pygame.transform.scale(pygame.image.load(os.path.join(ui_path,"inventory.png")),(128*constants.screen_scale,14*constants.screen_scale)))
inventory_ui.append({})
inventory_ui.append({})
for i in range(constants.INV_WIDTH*constants.INV_HEIGHT):
    button = Button(pygame.Rect(0,0,32*constants.screen_scale,32*constants.screen_scale),"inventory_item.png")
    button.surface = pygame.image.load(os.path.join(ui_path,button.path))
    surface2 = button.surface.copy()
    arr = pygame.PixelArray(surface2)
    arr.replace((192,111,219),(110,161,216))
    arr.replace((154,89,175),(88,129,173))
    arr.replace((103,71,114),(70,90,112))
    arr.close()
    button.down_surface = surface2
    button.surface = pygame.transform.scale(button.surface,(32*constants.screen_scale,32*constants.screen_scale))
    button.down_surface = pygame.transform.scale(button.down_surface,(32*constants.screen_scale,32*constants.screen_scale))
    button.rect.x = (i%constants.INV_WIDTH*34+43)*constants.screen_scale
    button.rect.y = (math.floor(i/constants.INV_WIDTH)*34+94)*constants.screen_scale
    inventory_ui[2].update({i:button})
for i in range(3):
    button = Button(pygame.Rect(0,0,32*constants.screen_scale,32*constants.screen_scale),"inventory_item.png")
    button.surface = pygame.image.load(os.path.join(ui_path,button.path))
    surface2 = button.surface.copy()
    arr = pygame.PixelArray(surface2)
    arr.replace((192,111,219),(110,161,216))
    arr.replace((154,89,175),(88,129,173))
    arr.replace((103,71,114),(70,90,112))
    arr.close()
    button.down_surface = surface2
    button.surface = pygame.transform.scale(button.surface,(32*constants.screen_scale,32*constants.screen_scale))
    button.down_surface = pygame.transform.scale(button.down_surface,(32*constants.screen_scale,32*constants.screen_scale))
    button.rect.x = (34*i+43)*constants.screen_scale
    button.rect.y = 42*constants.screen_scale
    inventory_ui[3].update({i:button})
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
                common.menu = "seed"
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
def seed():
    global menu_ticks
    constants.menu_surface.fill((0,1,0))
    constants.menu_surface.blit(seed_ui[16],(width_eighth,height_eighth/2))
    constants.menu_surface.blit(seed_ui[17],(width_eighth*1.25,height_eighth*0.875))
    for i in range(16):
        if (seed_ui[i].rect.collidepoint(pygame.mouse.get_pos()) and common.KeyDirect("mouse1")) or common.KeyDirect(eval("pygame.K_"+seed_ui[i].path[5])):
            if len(seed_ui[18])<=16:
                seed_ui[18].append(seed_ui[i].path[5])
    for i in range(16):
        seed_ui[i].Draw()
    if common.KeyDirect(pygame.K_BACKSPACE):
        if len(seed_ui[18])>=2:
            seed_ui[18].pop()
        elif len(seed_ui[18])==1:
            seed_ui[18]=[]
    if common.KeyDirect(pygame.K_RETURN):
        common.menu = None
        if len(seed_ui[18])==0:
            seed_ui[18] = "0000000000000000"
        e = ""
        for i in seed_ui[18]:
            e+=i
        if len(e)<16:
            seed_ui[18]+="0"*(16-len(e))
        common.run.reload(0,int(e,16))
    common.Font((0,1,0),pygame.Rect(width_eighth*3.25,height_eighth,width_eighth*4.75,height_eighth*2),seed_ui[18]+[None],2,constants.menu_surface)
def inventory():
    constants.menu_surface.fill((0,0,0))
    constants.menu_surface.blit(inventory_ui[1],(width_eighth*4-(inventory_ui[1].get_width()/2),height_eighth*0.25))
    constants.menu_surface.blit(inventory_ui[0],(width_eighth,height_eighth))
    pygame.draw.rect(constants.menu_surface,(0,1,0),pygame.Rect(inventory_ui[2][0].rect.x-constants.screen_scale,inventory_ui[2][0].rect.y-constants.screen_scale,34*constants.INV_WIDTH*constants.screen_scale,34*constants.INV_HEIGHT*constants.screen_scale))
    pygame.draw.rect(constants.menu_surface,(0,1,0),pygame.Rect(inventory_ui[3][0].rect.x-constants.screen_scale,inventory_ui[3][0].rect.y-constants.screen_scale,102*constants.screen_scale,34*constants.screen_scale))
    common.Font((0,1,0),pygame.Rect(72*constants.screen_scale,30*constants.screen_scale,150*constants.screen_scale,100*constants.screen_scale),"actions ",2,constants.menu_surface)
    common.Font((0,1,0),pygame.Rect(106*constants.screen_scale,81*constants.screen_scale,150*constants.screen_scale,100*constants.screen_scale),"storage ",2,constants.menu_surface)
    for i in inventory_ui[2]:
        inventory_ui[2][i].Draw()
        if inventory_ui[2][i].rect.collidepoint(pygame.mouse.get_pos()) and common.PressedKeys["mouse1"]:
            common.player.inventory["cursor"],common.player.inventory["inv_"+str(i)] = common.player.inventory["inv_"+str(i)],common.player.inventory["cursor"]
    for i in inventory_ui[3]:
        inventory_ui[3][i].Draw()
        if inventory_ui[3][i].rect.collidepoint(pygame.mouse.get_pos()) and common.PressedKeys["mouse1"]:
            common.player.inventory["cursor"],common.player.inventory["main_"+str(i)] = common.player.inventory["main_"+str(i)],common.player.inventory["cursor"]
    for i in common.player.inventory.keys():
        if type(common.player.inventory[i])==items.Item and i!="cursor":
            if i.startswith("inv_"):
                constants.menu_surface.blit(common.player.inventory[i].inv_texture,inventory_ui[2][int(i[4])])
            else:
                constants.menu_surface.blit(common.player.inventory[i].inv_texture,inventory_ui[3][int(i[5])])
    if type(common.player.inventory["cursor"])==items.Item:
        constants.menu_surface.blit(common.player.inventory["cursor"].inv_texture,pygame.mouse.get_pos())
    if common.PressedKeys[pygame.K_ESCAPE]:
        common.menu = None