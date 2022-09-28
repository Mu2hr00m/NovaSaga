from assets.managers import constants
from assets.managers import ai
from assets.managers import animation
import random
import math
import pygame
import os
import json
boxes = []
level_transitions = []
enemies = []
def new_enemy(x,y,maxhp,type,xp=0):
    enemy = Entity(type,type,xp)
    enemy.x = x
    enemy.y = y
    enemy.max_hp = maxhp
    enemy.hp = maxhp
    if type=="mite":
        enemy.max_speed = constants.MAX_SPEED*1.4
    enemy.update_physics()
    if len(enemies)==0:
        enemies.append(enemy)
    else:
        for i in range(len(enemies)):
            if enemies[i]==None:
                enemy.index = i
                enemies[i] = enemy
                break
            elif i==len(enemies)-1:
                enemy.index = i+1
                enemies.append(enemies)
class Ticker():
    def __init__(self,threshold):
        self.threshold = threshold
        self.tick = -1
        self.active = False
    def Tick(self,amount=1):
        if self.tick>=0:
            self.tick+=amount
        if self.tick>=self.threshold:
            self.tick = -1
            self.active = False
    def Trigger(self):
        if self.tick==-1:
            self.tick = 0
            self.active = True
    def Reset(self):
        self.tick = -1
class TransitionObject():
    def __init__(self,rect,dest,dest_level):
        self.rect = rect
        self.dest = dest
        self.dest_level = dest_level
    def check(self):
        if self.rect.collidepoint((player.x,player.y)):
            level.load(self.dest_level)
            player.x = self.dest[0]
            player.y = self.dest[1]
class DynamicTransitionObject():
    def __init__(self,rect,id,dest):
        self.rect = rect
        self.id = id
        self.dest = dest
        if self.id==0:
            self.dest_id = 2
        elif self.id==1:
            self.dest_id = 3
        elif self.id==2:
            self.dest_id = 0
        else:
            self.dest_id = 1
    def check(self):
        if self.rect.collidepoint((player.x,player.y)):
            if self.id==0:
                try:
                    level.load(run.intermediary.unloadedLevels[(level.global_position[0],level.global_position[1]-2)].level_id)
                except AttributeError:
                    level.load("test")
                    print("No valid level could be loaded at "+str(level.global_position[0])+", "+str(level.global_position[1]-2)+", so the default level was loaded")
            elif self.id==1:
                try:
                    level.load(run.intermediary.unloadedLevels[(level.global_position[0]+2,level.global_position[1])].level_id)
                except AttributeError:
                    level.load("test")
                    print("No valid level could be loaded at "+str(level.global_position[0]+2)+", "+str(level.global_position[1])+", so the default level was loaded")
            elif self.id==2:
                try:
                    level.load(run.intermediary.unloadedLevels[(level.global_position[0],level.global_position[1]+2)].level_id)
                except AttributeError:
                    level.load("test")
                    print("No valid level could be loaded at "+str(level.global_position[0])+", "+str(level.global_position[1]+2)+", so the default level was loaded")
            elif self.id==3:
                try:
                    level.load(run.intermediary.unloadedLevels[(level.global_position[0]-2,level.global_position[1])].level_id)
                except AttributeError:
                    level.load("test")
                    print("No valid level could be loaded at "+str(level.global_position[0]-2)+", "+str(level.global_position[1])+", so the default level was loaded")
            else:
                raise ValueError("Invalid transition id")
            if len(level_transitions)==0:
                raise ValueError("Destination level has no valid entrance")
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
class Entity():
    def apply_pallet(self,surface):
        for i in range(0,surface.get_width()):
            for j in range(0,surface.get_height()):
                if surface.get_at((i,j))==(128,0,0):
                    surface.set_at((i,j),self.pallet.get_at((0,0)))
                elif surface.get_at((i,j))==(255,0,0):
                    surface.set_at((i,j),self.pallet.get_at((1,0)))
                elif surface.get_at((i,j))==(255,128,0):
                    surface.set_at((i,j),self.pallet.get_at((2,0)))
                elif surface.get_at((i,j))==(255,255,0):
                    surface.set_at((i,j),self.pallet.get_at((3,0)))
                elif surface.get_at((i,j))==(128,128,0):
                    surface.set_at((i,j),self.pallet.get_at((4,0)))
                elif surface.get_at((i,j))==(0,128,0):
                    surface.set_at((i,j),self.pallet.get_at((5,0)))
                elif surface.get_at((i,j))==(0,255,0):
                    surface.set_at((i,j),self.pallet.get_at((6,0)))
                elif surface.get_at((i,j))==(0,255,128):
                    surface.set_at((i,j),self.pallet.get_at((7,0)))
                elif surface.get_at((i,j))==(0,128,128):
                    surface.set_at((i,j),self.pallet.get_at((8,0)))
        return surface
    def kill(self):
        enemies[self.index] = None
    def damage(self,amount=1):
        if not self.iframes.active:
            self.hp-=amount
            self.iframes.Trigger()
            if self.hp<=0:
                self.kill()
    def check_level(self,xp):
        level = 0
        while xp>level*100:
            level+=1
        low_thresh = (level-1)*100
        return (level,low_thresh,xp-low_thresh)
    def __init__(self,AItype="simple",texturepath="player",xp=0):
        self.iframes = Ticker(10)
        self.ground_drag = constants.DEF_GROUND_DRAG
        self.air_drag = constants.DEF_AIR_DRAG
        self.grav = constants.DEF_GRAVITY
        self.accel = constants.DEF_ACCEL
        self.air_accel = constants.DEF_AIR_ACCEL
        self.max_speed = constants.MAX_SPEED
        self.max_fall = constants.MAX_FALL
        self.jump = constants.DEF_JUMP
        self.anim_flip = False
        self.ai_type = AItype
        self.index = 0
        self.x = 0
        self.y = 0
        self.x_vel = 0
        self.y_vel = 0
        self.angle = 0
        self.max_hp = constants.DEF_HP
        self.hp = int(constants.DEF_HP/2)
        self.grounded_ticks = 0
        self.animation_ticks = Ticker(60)
        self.pallet = None
        self.texture_path = os.path.join("assets","sprites",texturepath)
        self.texture = None
        self.still_anim = None
        self.walking_anim = []
        self.falling_anim = []
        self.collisions = {"left":False,"right":False,"top":False,"bottom":False}
        self.has_jumped = False
        self.texture_size = [constants.HALF_BLOCK_SIZE,constants.HALF_BLOCK_SIZE]
        self.grounded = True
        self.hitbox = pygame.Rect(-constants.HALF_BLOCK_SIZE,-constants.HALF_BLOCK_SIZE,constants.BLOCK_SIZE,constants.BLOCK_SIZE)
        if AItype=="simple":
            self.AIpointer = ai.simple
            self.Animation = animation.simple
        if AItype=="player":
            self.AIpointer = ai.playerAI
            self.Animation = animation.player_anim
        if AItype=="mite":
            self.AIpointer = ai.mite
            self.Animation = animation.simple
        self.overlay_active = False
        self.xp = xp
        self.overlay = level.camera_surface.copy()
        self.overlay = pygame.transform.scale(self.overlay,(self.overlay.get_width()*3,self.overlay.get_height()*3))
        self.overlay.set_alpha(96)
        self.overlay.fill((0,0,0))
        pygame.draw.circle(self.overlay,(24,24,24),(self.overlay.get_width()/2,self.overlay.get_height()/2),128)
        pygame.draw.circle(self.overlay,(48,48,48),(self.overlay.get_width()/2,self.overlay.get_height()/2),64)
        pygame.draw.circle(self.overlay,(72,72,72),(self.overlay.get_width()/2,self.overlay.get_height()/2),32)
        self.pallet = pygame.image.load(os.path.join(self.texture_path,"pallet.png"))
        self.still_anim = self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"still.png")))
        self.walking_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"walking1.png"))))
        self.walking_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"walking2.png"))))
        self.walking_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"walking3.png"))))
        self.walking_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"walking4.png"))))
        self.walking_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"walking5.png"))))
        self.falling_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"falling1.png"))))
        self.falling_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"falling2.png"))))
        if self.ai_type=="player":
            self.animation_ticks.threshold = 50
            self.inventory = []
            self.arm_anim = []
            self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm1.png"))))
            self.arm_anim[0] = pygame.transform.scale(self.arm_anim[0],(self.arm_anim[0].get_width()*constants.screen_scale,self.arm_anim[0].get_height()*constants.screen_scale))
            self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm2.png"))))
            self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm3.png"))))
            self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm4.png"))))
            self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm5.png"))))
            self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm6.png"))))
            self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm7.png"))))
    
    def Draw(self):
        self.Animation(self)
    def collide(self,side="bottom"):
        collide = 0
        if side=="bottom":
            for i in range(0,self.hitbox.w):
                if level.collision.get_at((self.hitbox.x+i,self.hitbox.y+self.hitbox.h-1))==1:
                    collide +=1
        elif side=="grounded":
            for i in range(0,self.hitbox.w):
                if level.collision.get_at((self.hitbox.x+i,self.hitbox.y+self.hitbox.h))==1:
                    collide +=1
        elif side=="top":
            for i in range(0,self.hitbox.w):
                if level.collision.get_at((self.hitbox.x+i,self.hitbox.y))==1:
                    collide +=1
        elif side=="left":
            for i in range(1,self.hitbox.h-1):
                if level.collision.get_at((self.hitbox.x,self.hitbox.y+i))==1:
                    collide +=1
        elif side=="right":
            for i in range(1,self.hitbox.h-1):
                if level.collision.get_at((self.hitbox.x+self.hitbox.w-1,self.hitbox.y+i))==1:
                    collide +=1
        return collide
    def update_physics(self,up=False,left=False,right=False):
        self.iframes.Tick()
        if not (right or left):
            if self.grounded:
                self.x_vel *= self.ground_drag
            else:
                self.x_vel *= self.air_drag
        new_y_vel = self.y_vel + self.grav
        if not new_y_vel>=self.max_fall and not self.grounded:
            self.y_vel = new_y_vel
        if self.x_vel > self.max_speed:
            self.x_vel = self.max_speed
        if self.x_vel < -1*self.max_speed:
            self.x_vel = -1*self.max_speed
        if up and self.grounded_ticks>=-3 and self.has_jumped==False:
            self.y_vel -= self.jump
            self.has_jumped = True
            if self.y_vel>=self.jump:
                self.y_vel = -self.jump
        elif left and self.x_vel>-self.max_speed:
            if self.grounded:
                self.x_vel -= self.accel
            else:
                self.x_vel -= self.air_accel
        elif right and self.x_vel<self.max_speed:
            if self.grounded:
                self.x_vel += self.accel
            else:
                self.x_vel += self.air_accel
        if self.x+self.x_vel-(self.hitbox.w/2)<0:
            self.x=self.hitbox.w/2
            self.x_vel=0
        elif self.x+self.x_vel+(self.hitbox.w/2)>level.collision_texture.get_width():
            self.x=level.collision_texture.get_width()-(self.hitbox.w/2)
            self.x_vel=0
        else:
            self.x += self.x_vel
        if self.y+self.y_vel-(self.hitbox.h/2)<0:
            self.y=self.hitbox.h/2
            self.y_vel=0
        elif self.y+self.y_vel+(self.hitbox.h/2)>level.collision_texture.get_height():
            self.y=level.collision_texture.get_height()-(self.hitbox.h/2)
            self.y_vel=0
        else:
            self.y += self.y_vel
        
        if self.x_vel<=0.01 and self.x_vel>=-0.01:
            self.x_vel = 0
        self.hitbox.x = self.x-self.texture_size[0]
        self.hitbox.y = self.y-self.texture_size[1]
        still_colliding = True
        while still_colliding:
            still_colliding=False
            if self.collide("bottom")>=2:
                self.collisions["bottom"]=True
                self.y-=1
                self.hitbox.y-=1
                still_colliding=True
                if self.y_vel>0:
                    self.y_vel=0
            else:
                self.collisions["bottom"]=False
            if self.collide("top")>=2:
                self.collisions["top"]=True
                self.y+=1
                self.hitbox.y+=1
                still_colliding=True
                if self.y_vel<0:
                    self.y_vel=0
            else:
                self.collisions["top"]=False
            if self.collide("left")>=2:
                self.collisions["left"]=True
                self.x+=1
                self.hitbox.x+=1
                still_colliding=True
                if self.x_vel>0:
                    self.x_vel=0
            elif not self.grounded:
                self.collisions["left"]=False
            if self.collide("right")>=2:
                self.collisions["right"]=True
                self.x-=1
                self.hitbox.x-=1
                still_colliding=True
                if self.x_vel<0:
                    self.x_vel=0
            elif not self.grounded:
                self.collisions["right"]=False
            if self.collide("grounded")>=1:
                self.grounded = True
                self.has_jumped = False
            else:
                self.grounded = False
            if self.grounded:
                if self.grounded_ticks<0:
                    self.grounded_ticks = 0
                else:
                    self.grounded_ticks+=1
            else:
                if self.grounded_ticks>0:
                    self.grounded_ticks = 0
                else:
                    self.grounded_ticks-=1
        w_offset = -constants.screen_scale/2
        h_offset = -constants.screen_scale
        pos = (int((self.x-level.camera[0])*constants.screen_scale+w_offset),int((self.y-level.camera[1])*constants.screen_scale+h_offset))
        angle = math.degrees(math.atan((pygame.mouse.get_pos()[1]-pos[1])/(int(pygame.mouse.get_pos()[0]-pos[0])+0.1)))
        if pos[0]<=pygame.mouse.get_pos()[0]:
            angle -=180
        angle+=180
        self.angle = angle
class Item():
    def __init__(self,id,type,texture,on_use,cooldown):
        self.id = id
        self.type = type
        self.cooldown = cooldown
        self.texture = pygame.image.load(os.path.join(constants.ITEM_PATH,texture))
        self.texture = pygame.transform.scale(self.texture,(self.texture.get_width()*constants.screen_scale,self.texture.get_height()*constants.screen_scale))
        self.on_use = on_use
class Box():
    def __init__(self,rect):
        self.rect = rect
        self.hidden = False
    def Draw(self,forcedraw=False):
        if not self.hidden or forcedraw: #check wheter or not the box is hidden, or if its being forced to draw
            neg_player_y = int(-player.y+4)  #unflip player y and the rect y positions
            player_x = int(player.x)+0.5
            player_y = int(player.y-4)
            point9 = None
            camera_height = level.camera_surface.get_height() #get camera values, used to keep the drawn polygons onscreen
            camera_width = level.camera_surface.get_width()
            camera_x = level.camera_surface.get_offset()[0]
            camera_y = level.camera_surface.get_offset()[1]
            e = level.camera_surface.get_rect() #prepare for checking whether or not the box is onscreen
            e.x = camera_x
            e.y = camera_y
            x = self.rect.x
            y = self.rect.y
            x2 = x+self.rect.w
            y2 = y+self.rect.h
            if self.rect.colliderect(e): #check if the box is onscreen
                if x<camera_x: #constrain the x and y to within the screen
                    x=camera_x-1
                if x2>camera_x+camera_width:
                    x2=camera_x+camera_width+1
                if y<camera_y:
                    y=camera_y-1
                if y2>camera_y+camera_height:
                    y2=camera_y+camera_height+1
                if player_x>x2: #prepare some x positions for the screen edges
                    x_value_1 = camera_x
                    x_value_2 = camera_x
                elif player_x>x and player.y>y2:
                    x_value_1 = camera_width+camera_x
                    x_value_2 = camera_x
                elif player_x>x and player.y<y:
                    x_value_1 = camera_x
                    x_value_2 = camera_width+camera_x
                else:
                    x_value_1 = camera_width+camera_x
                    x_value_2 = camera_width+camera_x
                if player_y<=y and player_x>=x2: #determine where the player is in relation to the box
                    point1 = (x,-y)              #then thats used to place the proper points on the box
                    point2 = (x2,-y2)
                    point8 = (x,y2)
                elif player_y>=y2+1 and player_x>=x2:
                    point1 = (x2,-y)
                    point2 = (x,-y2)
                    point8 = (x,y)
                elif player_y>=y2+1 and player_x<=x:
                    point1 = (x2,-y2)
                    point2 = (x,-y)
                    point8 = (x2,y)
                elif player_y<=y and player_x<=x:
                    point1 = (x,-y2)
                    point2 = (x2,-y)
                    point8 = (x2,y2)
                elif player_y<=y:
                    point1 = (x2,-y)
                    point2 = (x,-y)
                    point8 = (x2,y2)
                    point9 = (x, y2)
                elif player_x>x2:
                    point1 = (x2,-y)
                    point2 = (x2,-y2)
                    point8 = (x,y)
                    point9 = (x,y2)
                elif player_y>=y2+1:
                    point1 = (x,-y2)
                    point2 = (x2,-y2)
                    point8 = (x,y)
                    point9 = (x2,y)
                elif player_x<=x:
                    point1 = (x,-y2)
                    point2 = (x,-y)
                    point8 = (x2,y2)
                    point9 = (x2,y)
                else:
                    point1 = (x,-y)
                    point2 = (x,-y)
                    point8 = (x,y)
                slope2 = (point1[1]-neg_player_y)/(point1[0]-player_x) #compute the slopes, for use later
                slope1 = (point2[1]-neg_player_y)/(point2[0]-player_x)
                y_value1 = -(neg_player_y-((player_x-x_value_1)*slope1)) #compute the y values, using adjusted point-slope form
                y_value2 = -(neg_player_y-((player_x-x_value_2)*slope2)) #2 x values, a y value, and a slope
                if y_value1<=camera_y:  #check if the y values are offscreen, and if they are, set the y value within the screen
                    y_value1 = camera_y #and compute the x value for where that line intersects the y value
                    x_value_1 = player_x-((neg_player_y+camera_y)/slope1)
                elif y_value1>=camera_height+camera_y:
                    y_value1 = camera_height+camera_y
                    x_value_1 = player_x-((neg_player_y+camera_height+camera_y)/slope1)
                if y_value2<=camera_y:
                    y_value2 = camera_y
                    x_value_2 = player_x-((neg_player_y+camera_y)/slope2)
                elif y_value2>=camera_height+camera_y:
                    y_value2 = camera_height+camera_y
                    x_value_2 = player_x-((neg_player_y+camera_height+camera_y)/slope2)
                point1 = (point1[0],-point1[1]) #compensate for the reversed y-axis
                point2 = (point2[0],-point2[1])
                if point1==(x2,y):
                    point1 = (point1[0]-1,point1[1])
                elif point1==(x2,y2):
                    point1 = (point1[0]-1,point1[1]-1)
                elif point1==(x,y2):
                    point1 = (point1[0],point1[1]-1)
                if point2==(x2,y):
                    point2 = (point2[0]-1,point2[1])
                elif point2==(x2,y2):
                    point2 = (point2[0]-1,point2[1]-1)
                elif point2==(x,y2):
                    point2 = (point2[0],point2[1]-1)
                point3 = (x_value_1,y_value1) #write some points, these are the edge points
                point4 = (x_value_2,y_value2)
                points = [point1,point8]
                if point9!=None:
                    points.append(point9)
                points.append(point2)
                points.append(point3)
                if not (y_value1==y_value2 or x_value_1==x_value_2):  #adds extra points in the corners where needed, else there'll be a triangular gap
                    if (y_value1==camera_y and y_value2==camera_height+camera_y) or (y_value1==camera_height+camera_y and y_value2==camera_y): #whenever 1 y value leaves the screen and the other doesn't
                        if player_x>=x: #statements with 2 points being made account for the rare scenario in which points are on opposite edges
                            points.append((camera_x,camera_height+camera_y))
                            points.append((camera_x,camera_y))
                        else:
                            points.append((camera_width+camera_x,camera_y))
                            points.append((camera_width+camera_x,camera_height+camera_y))
                    elif (x_value_1==camera_x and x_value_2==camera_width+camera_x) or (x_value_1==camera_width+camera_x and x_value_2==camera_x):
                        if player_y>=y:                                       #account for points on adjacent edges
                            points.append((camera_width+camera_x,camera_y))
                            points.append((camera_x,camera_y))
                        else:
                            points.append((camera_x,camera_height+camera_y))
                            points.append((camera_width+camera_x,camera_height+camera_y))
                    elif y_value2==camera_y or y_value2==camera_height+camera_y: #accounts for the points being on adjacent edges
                        points.append((x_value_1,y_value2))
                    else:
                        points.append((x_value_2,y_value1))
                points.append(point4)
                pygame.draw.polygon(constants.WIN,(0,0,0),points)
                #pygame.draw.line(constants.WIN,(0,0,0),point1,point4,1)
                #pygame.draw.line(constants.WIN,(0,0,0),point2,point3,1)
                #draw the polygon (finally)
    def afterdraw(self):
        pygame.draw.rect(constants.WIN,(3,33,3),self.rect)
class UnloadedLevel():
    def __init__(self,level_id,pos):
        self.level_id = level_id
        self.pos = pos
    def load(self):
        level.load(self.level_id)
        level.global_position = self.pos
class Level():
    def load(self,levelname="test"):
        path = open(os.path.join("assets","levels",levelname,"data.json"))
        data = json.load(path)                                                 #load level data.json
        self.display_texture = pygame.image.load(os.path.join("assets","levels",levelname,"display.png")) #load level, then scale it up on next line
        self.display_texture = pygame.transform.scale(self.display_texture,(self.display_texture.get_width()*data["level_scale"],self.display_texture.get_height()*data["level_scale"]))
        self.collision_texture = pygame.image.load(os.path.join("assets","levels",levelname,"display.png")) #load collision map, then scale it up on next line
        self.collision_texture = pygame.transform.scale(self.collision_texture,(self.collision_texture.get_width()*data["level_scale"],self.collision_texture.get_height()*data["level_scale"]))
        self.collision = pygame.mask.from_surface(self.collision_texture) #make collision
        self.camera = [0,0]                                               #make camera
        constants.WIN = pygame.transform.scale(constants.WIN,(self.display_texture.get_size())) #make the main level surface from the display texture
        self.camera_surface = constants.WIN.subsurface(0,0,constants.CAM_WIDTH,constants.CAM_HEIGHT) #make the camera, which is a subsurface of the level surface
        self.hud = pygame.surface.Surface((constants.disp_win.get_width(),constants.disp_win.get_height())) #make a hud, where hp and such will go
        self.hud.set_colorkey((0,0,0,255)) #allow hud to be transparent
        boxes.clear()                      #clear out various lists, in case they have stuff left over from the previous level
        level_transitions.clear()
        enemies.clear()
        try:
            for i in data["boxes"]:
                boxes.append(Box(pygame.Rect(i["x"],i["y"],i["w"],i["h"]))) #add extra boxes w/o collision
        except:
            pass
        try:
            for i in data["level_transitions"]:
                if i["style"]=="old":
                    level_transitions.append(TransitionObject(pygame.Rect(i["x"],i["y"],i["w"],i["h"]),(i["dest_x"],i["dest_y"]),i["dest_level"])) #add level transitions
                else:
                    level_transitions.append(DynamicTransitionObject(pygame.Rect(i["x"],i["y"],i["w"],i['h']),i["transition_id"],(i["dest_x"],i["dest_y"])))
        except:
            pass
        try:
            for i in data["enemies"]:
                new_enemy(i["x"],i["y"],i["hp"],i["type"]) #add enemies
        except:
            pass
        self.global_position = (0,0)
        print(level_transitions)
        k=0
        m=0
        boxrectlist = []                                                     #all this is the algorithm for making the boxes
        for i in range(0,self.collision_texture.get_width()-1):              #for each x
            for j in range(0,self.collision_texture.get_height()-1):         #for each y
                rect = pygame.Rect(i,j,1,1)
                if rect.collidelist(boxrectlist)==-1 and self.collision.get_at((i,j))==1: #check the point isnt already in a box
                    newbox= pygame.Rect(i,j,1,1)  #make a box
                    k=0
                    while True:
                        if newbox.x+k<constants.WIN.get_width()-1:         #go as far right as possible
                            if self.collision.get_at((newbox.x+k,j))==0:
                                break
                        else:
                            break
                        if k>constants.MAX_RECT_SIZE:
                            break
                        k+=1
                    newbox.w=k #set the width
                    newbox.h=constants.WIN.get_height()-newbox.y-1
                    for l in range(newbox.x,newbox.x+newbox.w):         #go as far down as possible, keeping the shortest column for the height
                        m=0
                        while True:
                            if not (l>constants.WIN.get_width()-1 or newbox.y+m>constants.WIN.get_height()-1):
                                if self.collision.get_at((l,newbox.y+m))==0:
                                    break
                            else:
                                break
                            if m>=newbox.h or m>constants.MAX_RECT_SIZE:
                                break
                            m+=1
                        newbox.h=m
                    if not (newbox.w==0 or newbox.h==0): #check that the rect isnt invalid
                        boxrectlist.append(newbox)       #then add the box
        for i in boxrectlist:     #for every rect in the box list, make an actual Box class
            boxes.append(Box(i))
    def update_camera(self,pos=None):
        if pos!=None:                #make a hook for placing the camera wherever
            self.camera[0] = pos[0]
            self.camera[1] = pos[1]
        else:
            self.camera = [int(player.x-(constants.CAM_WIDTH/2)),int(player.y-(constants.CAM_HEIGHT/2))] #set the camera to put the player in the middle
        if self.camera[0]<=0:          #constrain the camera to within the level borders, else game crash
            self.camera[0] = 0
        if self.camera[0]+constants.CAM_WIDTH>=constants.WIN.get_width():
            self.camera[0] = constants.WIN.get_width()-constants.CAM_WIDTH
        if self.camera[1]<=0:
            self.camera[1] = 0
        if self.camera[1]+constants.CAM_HEIGHT>=constants.WIN.get_height():
            self.camera[1] = constants.WIN.get_height()-constants.CAM_HEIGHT
        self.camera_surface = constants.WIN.subsurface(self.camera[0],self.camera[1],constants.CAM_WIDTH,constants.CAM_HEIGHT) #update the camera subsurface

class Node():
    def __init__(self,pos,type,maxconnections,owner): #not really used, might be used later
        self.pos = pos
        self.type = type
        self.maxconnections = maxconnections
        self.owner = owner
        self.connections = []
    def check(self,node):
        made_connection = False
        if len(self.connections)<self.maxconnections and len(node.connections)<node.maxconnections and self.connections.count(node)==0:
            self.connections.append(node)
            node.connections.append(self)
            self.owner.path(self.pos,node.pos)
            made_connection = True
        return made_connection
class Map():
    def GrowingTree(surface,extraconnections=1000): #maze generation algorithm
        pos = (random.randint(0,int(surface.get_width()/2))*2-1,random.randint(0,int(surface.get_height()/2))*2-1)
        allvisited = [pos]
        visited = [pos]
        while visited!=[]:
            valid_pos = [False,False,False,False]
            if pos[1]-2>0: #check the positions around it to see if they were visited
                if allvisited.count((pos[0],pos[1]-2))==0:
                    valid_pos[0]=True
            if pos[0]+2<surface.get_width():
                if allvisited.count((pos[0]+2,pos[1]))==0:
                    valid_pos[1]=True
            if pos[1]+2<surface.get_height():
                if allvisited.count((pos[0],pos[1]+2))==0:
                    valid_pos[2]=True
            if pos[0]-2>0:
                if allvisited.count((pos[0]-2,pos[1]))==0:
                    valid_pos[3]=True
            if valid_pos==[False,False,False,False]: #if all tiles adjacent are visited, remove from the visited list
                visited.remove(pos)
            else:
                while True: #else, randomly choose a valid pos and advance in that direction
                    value = random.randint(0,3)
                    if value==0 and valid_pos[0]:
                        newpos = (pos[0],pos[1]-2)
                        break
                    elif value==1 and valid_pos[1]:
                        newpos = (pos[0]+2,pos[1])
                        break
                    elif value==2 and valid_pos[2]:
                        newpos = (pos[0],pos[1]+2)
                        break
                    elif value==3 and valid_pos[3]:
                        newpos = (pos[0]-2,pos[1])
                        break
                    if valid_pos==[False,False,False,False]:
                        break
                visited.append(newpos)
                allvisited.append(newpos)
                pygame.draw.line(surface,constants.PATH_TILE_COLOR,pos,newpos)
            if random.random()<=0.3 and len(visited)>0: #allow branches by allowing random teleportation
                pos = visited[random.randint(0,len(visited)-1)]
            else:
                if len(visited)>0: #most of the time, it will continue with the previous position
                    pos = visited[len(visited)-1]
        for i in range(0,extraconnections): #mess up the perfect maze by splattering with random connections
            pos = (random.randint(3,int(surface.get_width()/2))*2-3,random.randint(3,int(surface.get_height()/2))*2-3)
            value = random.randint(0,3)
            if value==0:
                pygame.draw.line(surface,constants.PATH_TILE_COLOR,pos,(pos[0],pos[1]-2))
            elif value==1:
                pygame.draw.line(surface,constants.PATH_TILE_COLOR,pos,(pos[0],pos[1]+2))
            elif value==2:
                pygame.draw.line(surface,constants.PATH_TILE_COLOR,pos,(pos[0]-2,pos[1]))
            else:
                pygame.draw.line(surface,constants.PATH_TILE_COLOR,pos,(pos[0]+2,pos[1]))
        return surface
    def __init__(self,seed,type=0):
        self.seed = seed
        self.type = type
        if self.type==0: #intermediary type
            self.map = pygame.Surface((99,99))
            self.map.fill(constants.MAP_BACKGROUND_COLOR)
            self.doorways = []
            self.doorways.append([49,49]) #start tile pos
            self.doorways.append([2*random.randint(5,15)-1,2*random.randint(5,15)-1]) #memory tile pos
            self.doorways.append([2*random.randint(20,30)-1,2*random.randint(5,15)-1]) #dream tile pos
            self.doorways.append([2*random.randint(35,45)-1,2*random.randint(5,15)-1]) #labyrinth tile pos
            self.doorways.append([2*random.randint(35,45)-1,2*random.randint(20,30)-1]) #fracture tile pos
            self.doorways.append([2*random.randint(35,45)-1,2*random.randint(35,45)-1]) #abstract tile pos
            self.doorways.append([2*random.randint(20,30)-1,2*random.randint(35,45)-1]) #abyss tile pos
            self.doorways.append([2*random.randint(5,15)-1,2*random.randint(35,45)-1]) #trauma tile pos, not what it seems
            self.doorways.append([2*random.randint(5,15)-1,2*random.randint(20,30)-1]) #awakening tile pos
            self.doorways.append([2*random.randint(30,35)-1,2*random.randint(20,30)-1]) #auric door tile pos, also the end of the game
            for i in range(len(self.doorways)): #make the pos' into Node objects
                self.doorways[i] = Node(self.doorways[i],"doorway",2,self)
            self.secretrooms = [] #secret rooms (orange tiles)
            for i in range(random.randint(3,6)):
                while True:
                    point = [2*random.randint(5,45)-1,2*random.randint(5,45)-1]
                    if self.map.get_at(point)==constants.MAP_BACKGROUND_COLOR:
                        break
                self.secretrooms.append(Node(point,"secret",1,self))
            self.map.blit(Map.GrowingTree(self.map),(0,0)) #generate the maze
            for i in self.secretrooms:                     #make sure secret rooms only have 1 tile connection
                self.map.set_at(i.pos,constants.SECRET_ROOM_TILE_COLOR)
                value = random.randint(0,3)
                self.map.set_at((i.pos[0]-1,i.pos[1]),constants.MAP_BACKGROUND_COLOR)
                self.map.set_at((i.pos[0],i.pos[1]-1),constants.MAP_BACKGROUND_COLOR)
                self.map.set_at((i.pos[0],i.pos[1]+1),constants.MAP_BACKGROUND_COLOR)
                self.map.set_at((i.pos[0]+1,i.pos[1]),constants.MAP_BACKGROUND_COLOR)
                if value==0:
                    self.map.set_at((i.pos[0]-1,i.pos[1]),constants.PATH_TILE_COLOR)
                elif value==1:
                    self.map.set_at((i.pos[0],i.pos[1]-1),constants.PATH_TILE_COLOR)
                elif value==2:
                    self.map.set_at((i.pos[0],i.pos[1]+1),constants.PATH_TILE_COLOR)
                else:
                    self.map.set_at((i.pos[0]+1,i.pos[1]),constants.PATH_TILE_COLOR)
            self.map.set_at(self.doorways[0].pos,constants.START_TILE_COLOR) #start tile
            self.map.set_at(self.doorways[1].pos,constants.MEMORY_TILE_COLOR) #memory tile
            self.map.set_at(self.doorways[2].pos,constants.DREAM_TILE_COLOR) #dream tile
            self.map.set_at(self.doorways[3].pos,constants.LABYRINTH_TILE_COLOR) #labyrinth tile
            self.map.set_at(self.doorways[4].pos,constants.FRACTURE_TILE_COLOR) #fracture tile
            self.map.set_at(self.doorways[5].pos,constants.ABSTRACT_TILE_COLOR) #abstract tile
            self.map.set_at(self.doorways[6].pos,constants.ABYSS_TILE_COLOR) #abyss tile
            self.map.set_at(self.doorways[7].pos,constants.TRAUMA_TILE_COLOR) #trauma tile
            self.map.set_at(self.doorways[8].pos,constants.AWAKENING_TILE_COLOR) #awakening tile
            self.map.set_at(self.doorways[9].pos,constants.AURIC_DOOR_TILE_COLOR) #auric door tile
            self.map.set_at((self.doorways[0].pos[0]-1,self.doorways[0].pos[1]),constants.MAP_BACKGROUND_COLOR)
            self.map.set_at((self.doorways[0].pos[0],self.doorways[0].pos[1]-1),constants.MAP_BACKGROUND_COLOR)
            self.map.set_at((self.doorways[0].pos[0],self.doorways[0].pos[1]+1),constants.MAP_BACKGROUND_COLOR)
            self.map.set_at((self.doorways[0].pos[0]+1,self.doorways[0].pos[1]),constants.PATH_TILE_COLOR)
            pygame.draw.rect(self.map,constants.PATH_TILE_COLOR,pygame.Rect(self.doorways[0].pos[0]-2,self.doorways[0].pos[1]-2,5,5),1)
            self.unloadedLevels = []
class Run():
    def __init__(self,difficulty,seed=0x00000000): #this object will be saved
        self.seed = seed
        random.seed(self.seed)
        self.difficulty = difficulty
        self.intermediary = Map(self.seed)
level = Level()
run = Run(1,random.randbytes(16))
level.load("start")
player = Entity("player","player") #make the player