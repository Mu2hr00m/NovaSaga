import pygame
from assets.managers import constants,common,level
import random
import math,os
def simple(self):
    pygame.draw.rect(constants.WIN,(0,128,128),self.hitbox)
def player_anim(self):
    keys = pygame.key.get_pressed()
    pygame.draw.rect(common.loaded_level.hud,(16,16,16),pygame.Rect(0,0,constants.screen_scale*24,constants.screen_scale*12))
    pygame.draw.rect(common.loaded_level.hud,(128,16,16),pygame.Rect(-constants.screen_scale,-constants.screen_scale,constants.screen_scale*25,constants.screen_scale*13,),constants.screen_scale)
    pygame.draw.rect(common.loaded_level.hud,(96,16,16),pygame.Rect(constants.screen_scale,constants.screen_scale,constants.screen_scale*21*(self.hp/self.max_hp),constants.screen_scale*9))
    pygame.draw.rect(common.loaded_level.hud,(16,16,16),pygame.Rect(common.loaded_level.hud.get_width()-constants.screen_scale*23,0,constants.screen_scale*24,constants.screen_scale*12))
    pygame.draw.rect(common.loaded_level.hud,(16,128,16),pygame.Rect(common.loaded_level.hud.get_width()-constants.screen_scale*24,-constants.screen_scale,constants.screen_scale*25,constants.screen_scale*13),constants.screen_scale)
    pygame.draw.rect(common.loaded_level.hud,(16,96,16),pygame.Rect(common.loaded_level.hud.get_width()-constants.screen_scale*22,constants.screen_scale,constants.screen_scale*21*(self.xp%100/100),constants.screen_scale*9))
    image = self.still_anim
    arm_image = self.arm_anim[1]
    x_vel = self.x_vel
    y_vel = self.y_vel
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
                image = self.walking_anim[0]
                arm_image = self.arm_anim[2]
            self.facing_away = False
        elif x_vel<self.accel:
            image = self.walking_anim[4]
            arm_image = self.arm_anim[2]
            self.facing_away = False
        elif self.animation_ticks.tick>=25:
            image = self.walking_anim[3]
            arm_image = self.arm_anim[3]
            self.facing_away = False
        elif self.animation_ticks.tick>=15:
            image = self.walking_anim[2]
            arm_image = self.arm_anim[4]
            self.facing_away = False
        elif self.animation_ticks.tick>=5:
            image = self.walking_anim[1]
            arm_image = self.arm_anim[2]
            self.facing_away = False
        if self.animation_ticks.tick>=35:
            self.animation_ticks.tick = 5
    else:
        if self.y_vel>0.7:
            image = self.falling_anim[1]
            arm_image = self.arm_anim[6]
            self.animation_ticks.Reset()
            self.facing_away = False
        elif self.y_vel>0:
            image = self.falling_anim[0]
            arm_image = self.arm_anim[5]
            self.animation_ticks.tick = 1
            self.facing_away = False
    #print(str(self.animation_ticks)+", "+str(self.x_vel))
    if pygame.mouse.get_focused() and pygame.mouse.get_pressed(5)[0]:
        arm_image = self.arm_anim[0]
        arm_image.blit(self.inventory["main_0"].texture,(int((arm_image.get_width()-constants.screen_scale)/2),int((arm_image.get_height()-constants.screen_scale)/2)))
        angle = self.angle
        w_offset = -constants.screen_scale/2
        h_offset = -constants.screen_scale*1.5
        pos = (int((self.x-common.loaded_level.camera[0])*constants.screen_scale+w_offset),int((self.y-common.loaded_level.camera[1])*constants.screen_scale+h_offset))
        if pygame.mouse.get_pos()[0]<pos[0]:
            self.anim_flip = True
        else:
            self.anim_flip = False
        angle-=180
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
        image = self.facing_away_img
    if self.anim_flip:
        image = pygame.transform.flip(image,True,False)
    constants.WIN.blit(image,(self.hitbox.x,self.hitbox.y+1))
    if not (pygame.mouse.get_focused() and pygame.mouse.get_pressed(5)[0]) and not self.facing_away:
        constants.WIN.blit(arm_image,(self.hitbox.x,self.hitbox.y+1))
    if keys[pygame.K_p]:
        common.run = level.Run(0,os.urandom(16))
    if keys[pygame.K_g]:
        common.loaded_level.hud.blit(pygame.transform.scale(common.run.intermediary.map,(common.run.intermediary.map.get_width()*(constants.screen_scale*2-1),common.run.intermediary.map.get_height()*(constants.screen_scale*2-1))),(0,0))
    if keys[pygame.K_h]:
        common.active_text = common.e
        common.active_text.is_open = True