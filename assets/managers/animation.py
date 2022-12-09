import pygame
from assets.managers import constants,common,level
import random
import math,os
def simple(self):
    pygame.draw.rect(constants.WIN,(0,128,128),self.hitbox)
def mite_anim(self):
    x_vel = self.x_vel
    y_vel = self.y_vel
    animation_type = 0
    image = self.spritesheet[1][0].copy()
    if x_vel<0:
        x_vel*=-1
    if y_vel<0:
        y_vel*=-1
    if self.x_vel<0:
        self.anim_flip = True
    elif self.x_vel>0:
        self.anim_flip = False
    if self.grounded:
        self.animation_ticks.Trigger()
        self.animation_ticks.Loop()
        if x_vel==0:
            self.animation_ticks.Reset()
        elif self.animation_ticks.tick<=0 and not common.out_of_bounds((self.hitbox.x-1,self.hitbox.y+self.hitbox.h-2)):
            if common.loaded_level.collision.get_at((self.hitbox.x-1,self.hitbox.y+self.hitbox.h-2))!=0 and common.loaded_level.collision.get_at((self.hitbox.x+self.hitbox.w+1,self.hitbox.y+self.hitbox.h-2))!=0:
                image = self.spritesheet[1][0].copy()
        elif self.animation_ticks.tick>=5:
            image = self.spritesheet[2][1].copy()
            animation_type = 1
        elif self.animation_ticks.tick>=0:
            image = self.spritesheet[2][0].copy()
            animation_type = 1
    else:
        if self.y_vel>0.7:
            image = self.spritesheet[3][1].copy()
            self.animation_ticks.Reset()
            animation_type = 2
        elif self.y_vel>0:
            image = self.spritesheet[3][0].copy()
            self.animation_ticks.tick = 1
            animation_type = 2
    if self.anim_flip:
        image = pygame.transform.flip(image,True,False)
    mask_relative = (self.x%10+5,self.y%10+5)
    mask = self.spritesheet[0][0].subsurface(pygame.Rect(mask_relative[0],mask_relative[1],10,10))
    for i in range(10):
        for j in range(10):
            if image.get_at((i,j))==(0,255,0):
                image.set_at((i,j),mask.get_at((i,j)))
    offset = self.spritesheet[animation_type]["offset"]
    constants.WIN.blit(image,(self.hitbox.x+offset[0],self.hitbox.y+offset[1]))
def player_anim(self):
    spritesheet = self.palletized_sprites[self.pallet]
    keys = pygame.key.get_pressed()
    pygame.draw.rect(common.loaded_level.hud,(16,16,16),pygame.Rect(0,0,constants.screen_scale*24,constants.screen_scale*12))
    pygame.draw.rect(common.loaded_level.hud,(128,16,16),pygame.Rect(-constants.screen_scale,-constants.screen_scale,constants.screen_scale*25,constants.screen_scale*13,),constants.screen_scale)
    pygame.draw.rect(common.loaded_level.hud,(96,16,16),pygame.Rect(constants.screen_scale,constants.screen_scale,constants.screen_scale*21*(self.hp/self.max_hp),constants.screen_scale*9))
    pygame.draw.rect(common.loaded_level.hud,(16,16,16),pygame.Rect(common.loaded_level.hud.get_width()-constants.screen_scale*23,0,constants.screen_scale*24,constants.screen_scale*12))
    pygame.draw.rect(common.loaded_level.hud,(16,128,16),pygame.Rect(common.loaded_level.hud.get_width()-constants.screen_scale*24,-constants.screen_scale,constants.screen_scale*25,constants.screen_scale*13),constants.screen_scale)
    pygame.draw.rect(common.loaded_level.hud,(16,96,16),pygame.Rect(common.loaded_level.hud.get_width()-constants.screen_scale*22,constants.screen_scale,constants.screen_scale*21*(self.xp%100/100),constants.screen_scale*9))
    image = spritesheet[0][0]
    arm_image = spritesheet[3][1]
    x_vel = self.x_vel
    y_vel = self.y_vel
    animation_type = 0
    if x_vel<0:
        x_vel*=-1
    if y_vel<0:
        y_vel*=-1
    if self.x_vel<0:
        self.anim_flip = True
    elif self.x_vel>0:
        self.anim_flip = False
    if self.grounded:
        self.animation_ticks.Trigger()
        self.animation_ticks.Tick()
        if x_vel==0:
            self.animation_ticks.Reset()
        elif self.animation_ticks.tick<=5 and not common.out_of_bounds((self.hitbox.x-1,self.hitbox.y+self.hitbox.h-2)):
            if common.loaded_level.collision.get_at((self.hitbox.x-1,self.hitbox.y+self.hitbox.h-2))!=0 and common.loaded_level.collision.get_at((self.hitbox.x+self.hitbox.w+1,self.hitbox.y+self.hitbox.h-2))!=0:
                image = spritesheet[1][0]
                arm_image = spritesheet[3][2]
            self.facing_away = False
        elif x_vel<self.accel:
            image = spritesheet[1][4]
            arm_image = spritesheet[3][2]
            self.facing_away = False
            animation_type = 1
        elif self.animation_ticks.tick>=25:
            image = spritesheet[1][3]
            arm_image = spritesheet[3][3]
            self.facing_away = False
            animation_type = 1
        elif self.animation_ticks.tick>=15:
            image = spritesheet[1][2]
            arm_image = spritesheet[3][4]
            self.facing_away = False
            animation_type = 1
        elif self.animation_ticks.tick>=5:
            image = spritesheet[1][1]
            arm_image = spritesheet[3][2]
            self.facing_away = False
            animation_type = 1
        if self.animation_ticks.tick>=35:
            self.animation_ticks.tick = 5
    else:
        if self.y_vel>0.7:
            image = spritesheet[2][1]
            arm_image = spritesheet[3][6]
            self.animation_ticks.Reset()
            self.facing_away = False
            animation_type = 2
        elif self.y_vel>0:
            image = spritesheet[2][0]
            arm_image = spritesheet[3][5]
            self.animation_ticks.tick = 1
            self.facing_away = False
            animation_type = 2
    using_something = False
    if common.GetPressed("action1") or common.GetPressed("action2") or common.GetPressed("action3"):
        using_something = True
        arm_image = spritesheet[3][0].copy()
        if common.GetPressed("action1") and self.inventory["main_0"]!=None:
            arm_image.blit(self.inventory["main_0"].texture,(int((arm_image.get_width()-constants.screen_scale)/2),int((arm_image.get_height()-constants.screen_scale)/2)))
        elif common.GetPressed("action2") and self.inventory["main_1"]!=None:
            arm_image.blit(self.inventory["main_1"].texture,(int((arm_image.get_width()-constants.screen_scale)/2),int((arm_image.get_height()-constants.screen_scale)/2)))
        elif common.GetPressed("action3") and self.inventory["main_2"]!=None:
            arm_image.blit(self.inventory["main_2"].texture,(int((arm_image.get_width()-constants.screen_scale)/2),int((arm_image.get_height()-constants.screen_scale)/2)))
        angle = self.angle
        w_offset = -constants.screen_scale/2
        h_offset = -constants.screen_scale*1.5
        pos = (int((self.x-common.loaded_level.camera[0])*constants.screen_scale+w_offset),int((self.y-common.loaded_level.camera[1])*constants.screen_scale+h_offset))
        if pygame.mouse.get_pos()[0]<pos[0]:
            self.anim_flip = True
        else:
            self.anim_flip = False
        angle-=180
        arm_image = common.Scale(arm_image)
        if not pos[0]<=pygame.mouse.get_pos()[0]:
            arm_image = pygame.transform.flip(arm_image,True,False)
        angle*=-1
        angle-=90
        arm_image = pygame.transform.rotate(arm_image,angle)
        pos = (pos[0]-arm_image.get_width()/2,pos[1]-arm_image.get_height()/2)
        common.loaded_level.hud.blit(arm_image,pos)
    else:
        if self.anim_flip:
            arm_image = pygame.transform.flip(arm_image,True,False)
    if self.facing_away:
        image = spritesheet[0][1]
    if self.anim_flip:
        image = pygame.transform.flip(image,True,False)
    offset = spritesheet[animation_type]["offset"]
    arm_offset = spritesheet[3]["offset"]
    constants.WIN.blit(image,(self.hitbox.x+offset[0],self.hitbox.y+offset[1]))
    if not using_something and not self.facing_away:
        constants.WIN.blit(arm_image,(self.hitbox.x+arm_offset[0],self.hitbox.y+arm_offset[1]))
    if keys[pygame.K_p]:
        common.run = level.Run(0,os.urandom(16))
    if keys[pygame.K_g]:
        common.loaded_level.hud.blit(common.Scale(common.run.intermediary_map,constants.screen_scale*2-1),(0,0))
        if common.allticks%20<10:
            pygame.draw.rect(common.loaded_level.hud,(255,255,255),pygame.Rect(common.global_position[0]*(constants.screen_scale*2-1),common.global_position[1]*(constants.screen_scale*2-1),constants.screen_scale*2-1,constants.screen_scale*2-1))
    if keys[pygame.K_h]:
        common.active_text = common.e
        common.active_text.is_open = True