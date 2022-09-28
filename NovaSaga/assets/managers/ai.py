import pygame
from assets.managers import game_classes
from assets.managers import constants
def simple(self):
    self.update_physics()
def mite(self):
    up=False
    left=False
    right=False
    if game_classes.player.x<self.x-6:
        left=True
    elif game_classes.player.x>self.x+6:
        right=True
    if self.collisions["left"] or self.collisions["right"]:
        up=True
    if game_classes.player.x-18<self.x and game_classes.player.x+18>self.x and self.y>game_classes.player.y-8 and self.y< game_classes.player.y+8:
        up=True
    self.update_physics(up,left,right)
    if self.hitbox.colliderect(game_classes.player.hitbox):
        game_classes.player.damage(1)
def playerAI(self):
    keys = pygame.key.get_pressed()
    up=False
    left=False
    right=False
    if keys[pygame.K_w]:
        up=True
    if keys[pygame.K_a]:
        left=True
    if keys[pygame.K_d]:
        right=True
    if keys[pygame.K_SPACE]:
        print((self.x,self.y))
    if keys[pygame.K_ESCAPE]:
        constants.menu = "pause"
    if keys[pygame.K_UP] and self.hp<self.max_hp:
        self.hp+=1
    if keys[pygame.K_DOWN] and self.hp>0:
        self.damage(1)
    if keys[pygame.K_RIGHT]:
        self.xp+=1
    if keys[pygame.K_LEFT] and self.xp>0:
        self.xp-=1
    self.update_physics(up,left,right)
    for i in self.inventory:
        if i.type=="gun":
            i.cooldown.Tick()
    if pygame.mouse.get_focused():
        #game_classes.boxes[len(game_classes.boxes)-1].rect.x = pygame.mouse.get_pos()[0]
        #game_classes.boxes[len(game_classes.boxes)-1].rect.y = pygame.mouse.get_pos()[1]
        if pygame.mouse.get_pressed(5)[0] and keys[pygame.K_LSHIFT]:
            pos = pygame.mouse.get_pos()
            pos = [pos[0],pos[1]]
            pos[0] = int((pos[0]/constants.disp_win.get_width()*constants.CAM_WIDTH)+game_classes.level.camera[0])
            pos[1] = int((pos[1]/constants.disp_win.get_height()*constants.CAM_HEIGHT)+game_classes.level.camera[1])
            print(pos)
        elif pygame.mouse.get_pressed(5)[0]:
            self.inventory[0].on_use(self.inventory[0])