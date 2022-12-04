import pygame
from assets.managers import constants
from assets.managers import common
import math
import os
class Bullet():
    def __init__(self,x,y,angle,texture,speed,damage,pierce=0,bounce=0,gravity=constants.DEF_GRAVITY/3):
        self.x = x
        self.y = y
        self.x_vel = math.cos(math.radians(angle))*speed
        self.y_vel = math.sin(math.radians(angle))*speed
        self.speed = speed
        self.uuid = "0-0-0-0"
        self.texture = pygame.image.load(os.path.join(constants.PROJ_PATH,texture))
        self.index = 0
        self.damage = damage
        self.pierce = pierce
        self.bounce = bounce
        self.gravity = gravity
        self.damage_ticks = 0
    def kill(self):
        if common.delentities.count(self.uuid)==0:
            common.delentities.append(self.uuid)
    def update(self):
        if self.y_vel>10:
            self.y_vel=10
        else:
            self.y_vel+=self.gravity
        if not common.out_of_bounds((self.x,self.y),2) and not common.out_of_bounds((self.x+self.x_vel,self.y+self.y_vel),2):
            x_step = self.x_vel/self.speed
            y_step = self.y_vel/self.speed
            total_x=0
            total_y=0
            for i in range(self.speed):
                x=x_step*i+self.x
                y=y_step*i+self.y
                if common.loaded_level.collision.get_at((x,y))==1:
                    if common.loaded_level.collision.get_at((x,y+1))==1 and common.loaded_level.collision.get_at((x,y-1))==1:
                        x_step*=-1
                        self.x_vel=self.x_vel/2*-1
                    if common.loaded_level.collision.get_at((x+1,y))==1 and common.loaded_level.collision.get_at((x-1,y))==1:
                        y_step*=-1
                        self.y_vel*=-1
                        if self.y_vel<0:
                            self.y_vel/=2
                            y_step/=2
                    if self.bounce<=0:
                        self.kill()
                    self.bounce-=1
                total_x+=x_step
                total_y+=y_step
            self.x+=total_x
            self.y+=total_y
        else:
            self.kill()
        for i in common.entities:
            i = common.entities[i]
            if type(i)==common.Entity:
               if i.hitbox.collidepoint((self.x,self.y)):
                    i.damage(self.damage)
                    self.pierce-=1
                    if self.pierce<0:
                        self.kill()
    def Draw(self):
        constants.WIN.blit(self.texture,(self.x-1,self.y-1))