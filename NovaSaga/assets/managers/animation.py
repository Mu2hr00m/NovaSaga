import pygame
from assets.managers import constants
from assets.managers import game_classes
import random
import math
def simple(self):
    pygame.draw.rect(constants.WIN,(0,128,128),self.hitbox)
def player_anim(self):
    keys = pygame.key.get_pressed()
    pygame.draw.rect(game_classes.level.hud,(16,16,16),pygame.Rect(0,0,constants.screen_scale*24,constants.screen_scale*12))
    pygame.draw.rect(game_classes.level.hud,(128,16,16),pygame.Rect(-constants.screen_scale,-constants.screen_scale,constants.screen_scale*25,constants.screen_scale*13,),constants.screen_scale)
    pygame.draw.rect(game_classes.level.hud,(96,16,16),pygame.Rect(constants.screen_scale,constants.screen_scale,constants.screen_scale*21*(self.hp/self.max_hp),constants.screen_scale*9))
    pygame.draw.rect(game_classes.level.hud,(16,16,16),pygame.Rect(game_classes.level.hud.get_width()-constants.screen_scale*23,0,constants.screen_scale*24,constants.screen_scale*12))
    pygame.draw.rect(game_classes.level.hud,(16,128,16),pygame.Rect(game_classes.level.hud.get_width()-constants.screen_scale*24,-constants.screen_scale,constants.screen_scale*25,constants.screen_scale*13),constants.screen_scale)
    pygame.draw.rect(game_classes.level.hud,(16,96,16),pygame.Rect(game_classes.level.hud.get_width()-constants.screen_scale*22,constants.screen_scale,constants.screen_scale*21*(self.xp%100/100),constants.screen_scale*9))
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
        elif self.animation_ticks.tick<=15:
            image = self.walking_anim[0]
            arm_image = self.arm_anim[2]
        elif x_vel<self.accel:
            image = self.walking_anim[4]
            arm_image = self.arm_anim[2]
        elif self.animation_ticks.tick>=40:
            image = self.walking_anim[3]
            arm_image = self.arm_anim[3]
        elif self.animation_ticks.tick>=30:
            image = self.walking_anim[2]
            arm_image = self.arm_anim[4]
        elif self.animation_ticks.tick>=20:
            image = self.walking_anim[1]
            arm_image = self.arm_anim[2]
        if self.animation_ticks.tick>=49:
            self.animation_ticks.tick = 20
    else:
        if self.y_vel>0.7:
            image = self.falling_anim[1]
            arm_image = self.arm_anim[6]
            self.animation_ticks.Reset()
        elif self.y_vel>0:
            image = self.falling_anim[0]
            arm_image = self.arm_anim[5]
            self.animation_ticks.tick = 1
    if self.anim_flip:
        image = pygame.transform.flip(image,True,False)
        if not pygame.mouse.get_pressed(5)[0]:
            arm_image = pygame.transform.flip(arm_image,True,False)
    #print(str(self.animation_ticks)+", "+str(self.x_vel))
    constants.WIN.blit(image,(self.hitbox.x,self.hitbox.y))
    if pygame.mouse.get_focused()and pygame.mouse.get_pressed(5)[0]:
        arm_image = self.arm_anim[0]
        arm_image.blit(self.inventory[0].texture,(int((arm_image.get_width()-constants.screen_scale)/2),int((arm_image.get_height()-constants.screen_scale)/2)))
        angle = self.angle
        w_offset = -constants.screen_scale/2
        h_offset = -constants.screen_scale
        pos = (int((self.x-game_classes.level.camera[0])*constants.screen_scale+w_offset),int((self.y-game_classes.level.camera[1])*constants.screen_scale+h_offset))
        angle-=180
        if not pos[0]<=pygame.mouse.get_pos()[0]:
            arm_image = pygame.transform.flip(arm_image,True,False)
        angle*=-1
        angle-=90
        arm_image = pygame.transform.rotate(arm_image,angle)
        pos = (pos[0]-arm_image.get_width()/2,pos[1]-arm_image.get_height()/2)
        game_classes.level.hud.blit(arm_image,pos)
        
    else:
        constants.WIN.blit(arm_image,(self.hitbox.x,self.hitbox.y))
    if keys[pygame.K_f]:
        game_classes.run = game_classes.Run(1,random.randbytes(16))
    if keys[pygame.K_g]:
        game_classes.level.hud.blit(pygame.transform.scale(game_classes.run.intermediary.map,(game_classes.run.intermediary.map.get_width()*(constants.screen_scale*2-1),game_classes.run.intermediary.map.get_height()*(constants.screen_scale*2-1))),(0,0))