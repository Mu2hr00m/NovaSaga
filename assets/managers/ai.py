import pygame
from assets.managers import constants,common
def simple(self):
    self.update_physics()
def no_physics(self):
    pass
def mite(self):
    if self.has_control:
        up=False
        left=False
        right=False
        if common.player.x<self.x-6:
            left=True
        elif common.player.x>self.x+6:
            right=True
        if self.collisions["left"] or self.collisions["right"]:
            up=True
        if common.player.x-18<self.x and common.player.x+18>self.x and self.y>common.player.y-8 and self.y< common.player.y+8:
            up=True
        self.update_physics(up,left,right)
        if self.hitbox.colliderect(common.player.hitbox):
            common.player.damage(1)
    else:
        self.update_physics(False,False,False)
def playerAI(self):
    if self.has_control:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RSHIFT]:
            print((self.x,self.y))
        if keys[pygame.K_ESCAPE]:
            common.menu = "pause"
        if keys[pygame.K_UP] and self.hp<self.max_hp:
            self.hp+=1
        if keys[pygame.K_DOWN] and self.hp>0:
            self.damage(1)
        if keys[pygame.K_RIGHT]:
            self.xp+=1
        if keys[pygame.K_LEFT] and self.xp>0:
            self.xp-=1
        self.update_physics(common.GetPressed("jump"),common.GetPressed("left"),common.GetPressed("right"))
        for i in self.inventory:
            if self.inventory[i]!=None:
                self.inventory[i].cooldown.Tick()
        if common.GetPressed("action1") and self.inventory["main_0"]!=None:
            self.inventory["main_0"].on_use(self.inventory["main_0"])
        elif common.GetPressed("action2") and self.inventory["main_1"]!=None:
            self.inventory["main_1"].on_use(self.inventory["main_1"])
        elif common.GetPressed("action3") and self.inventory["main_2"]!=None:
            self.inventory["main_2"].on_use(self.inventory["main_2"])
        if common.GetPressed("inventory"):
            common.menu = "inventory"
        if pygame.mouse.get_focused():
            #game_classes.boxes[len(game_classes.boxes)-1].rect.x = pygame.mouse.get_pos()[0]
            #game_classes.boxes[len(game_classes.boxes)-1].rect.y = pygame.mouse.get_pos()[1]
            if pygame.mouse.get_pressed(5)[0] and keys[pygame.K_LSHIFT]:
                pos = pygame.mouse.get_pos()
                pos = [pos[0],pos[1]]
                color = constants.disp_win.get_at(pos)
                pos[0] = int((pos[0]/constants.disp_win.get_width()*constants.CAM_WIDTH)+common.loaded_level.camera[0])
                pos[1] = int((pos[1]/constants.disp_win.get_height()*constants.CAM_HEIGHT)+common.loaded_level.camera[1])
                print(pos,color)
    else:
        self.update_physics(False,False,False)