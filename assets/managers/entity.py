from assets.managers import constants
from assets.managers import common
from assets.managers import animation
from assets.managers import ai
import os,pathlib
import pygame
import math,time
class Entity():
    def apply_pallet(self,surface:pygame.Surface,pallet:pygame.Surface,rep_pallet:pygame.Surface)->pygame.Surface:
        arr = pygame.PixelArray(surface)
        for i in range(min(rep_pallet.get_width(),pallet.get_width())):
            arr.replace(rep_pallet.get_at((i,0)),pallet.get_at((i,0)))
        arr.close()
        return surface
    def kill(self):
        common.enemies[self.index] = None
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
        self.name = "NoName"
        self.iframes = common.Ticker(10)
        self.text_color = constants.CHAR_COLORS["default"]
        self.has_control = True
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
        self.portraits = {"default":pygame.transform.scale(pygame.image.load(os.path.join(constants.PORTRAIT_PATH,"default.png")),(32*constants.screen_scale,32*constants.screen_scale))}
        self.x = 0
        self.y = 0
        self.x_vel = 0
        self.y_vel = 0
        self.angle = 0
        self.max_hp = constants.DEF_HP
        self.hp = int(constants.DEF_HP/2)
        self.grounded_ticks = 0
        self.animation_ticks = common.Ticker(60)
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
            self.name = "nova"
        if AItype=="mite":
            self.AIpointer = ai.mite
            self.Animation = animation.simple
            self.name = "mite"
        for i in os.listdir(constants.PORTRAIT_PATH):
            item = i.split("-",1)
            if item[0]==self.name:
                self.portraits.update({item[1].split(".",1)[0]:pygame.transform.scale(pygame.image.load(os.path.join(constants.PORTRAIT_PATH,i)),(32*constants.screen_scale,32*constants.screen_scale))})
        print(self.portraits)
        self.overlay_active = False
        self.xp = xp
        self.overlay = common.loaded_level.camera_surface.copy()
        self.overlay = pygame.transform.scale(self.overlay,(self.overlay.get_width()*3,self.overlay.get_height()*3))
        self.overlay.set_alpha(96)
        self.overlay.fill((0,0,0))
        pygame.draw.circle(self.overlay,(24,24,24),(self.overlay.get_width()/2,self.overlay.get_height()/2),128)
        pygame.draw.circle(self.overlay,(40,40,40),(self.overlay.get_width()/2,self.overlay.get_height()/2),64)
        pygame.draw.circle(self.overlay,(64,64,64),(self.overlay.get_width()/2,self.overlay.get_height()/2),32)
        #self.pallet = pygame.image.load(os.path.join(self.texture_path,"pallet.png"))
        #self.still_anim = self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"still.png")),self.pallet)
        #self.walking_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"walking1.png")),self.pallet))
        #self.walking_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"walking2.png")),self.pallet))
        #self.walking_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"walking3.png")),self.pallet))
        #self.walking_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"walking4.png")),self.pallet))
        #self.walking_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"walking5.png")),self.pallet))
        #self.falling_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"falling1.png")),self.pallet))
        #self.falling_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"falling2.png")),self.pallet))
        if self.ai_type=="player":
            self.text_color = constants.CHAR_COLORS["nova"]
            self.animation_ticks.threshold = 35
            self.inventory = {"main_1":None,"main_2":None,"main_3":None}
            self.portraits.update({"happy":pygame.transform.scale(pygame.image.load(os.path.join(constants.PORTRAIT_PATH,"nova-happy.png")),(32*constants.screen_scale,32*constants.screen_scale))})
            self.portraits.update({"neutral":pygame.transform.scale(pygame.image.load(os.path.join(constants.PORTRAIT_PATH,"nova-neutral.png")),(32*constants.screen_scale,32*constants.screen_scale))})
            self.portraits.update({"sad":pygame.transform.scale(pygame.image.load(os.path.join(constants.PORTRAIT_PATH,"nova-sad.png")),(32*constants.screen_scale,32*constants.screen_scale))})
            for i in range(constants.INV_WIDTH*constants.INV_HEIGHT-1):
                self.inventory.update({"inv_"+str(i):None})
            self.spritesheet = common.Spritesheet(os.path.join("assets","sprites","player_sprites.png"))
            self.still_anim = self.apply_pallet(self.spritesheet[0][0],self.spritesheet["pallets"][1],self.spritesheet["pallets"][0])
            self.facing_away_img = self.apply_pallet(self.spritesheet[0][1],self.spritesheet["pallets"][1],self.spritesheet["pallets"][0])
            self.facing_away = False
            self.walking_anim = []
            self.falling_anim = []
            self.arm_anim = []
            for i in self.spritesheet[1]:
                if type(self.spritesheet[1][i])==pygame.Surface:
                    self.walking_anim.append(self.apply_pallet(self.spritesheet[1][i],self.spritesheet["pallets"][1],self.spritesheet["pallets"][0]))
            for i in self.spritesheet[2]:
                if type(self.spritesheet[2][i])==pygame.Surface:
                    self.falling_anim.append(self.apply_pallet(self.spritesheet[2][i],self.spritesheet["pallets"][1],self.spritesheet["pallets"][0]))
            for i in self.spritesheet[3]:
                if type(self.spritesheet[3][i])==pygame.Surface:
                    self.arm_anim.append(self.apply_pallet(self.spritesheet[3][i],self.spritesheet["pallets"][1],self.spritesheet["pallets"][0]))
            print(self.arm_anim)
            #self.facing_away_img = self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"away_still.png")),self.pallet)
            #self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm1.png")),self.pallet))
            #self.arm_anim[0] = pygame.transform.scale(self.arm_anim[0],(self.arm_anim[0].get_width()*constants.screen_scale,self.arm_anim[0].get_height()*constants.screen_scale))
            #self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm2.png")),self.pallet))
            #self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm3.png")),self.pallet))
            #self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm4.png")),self.pallet))
            #self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm5.png")),self.pallet))
            #self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm6.png")),self.pallet))
            #self.arm_anim.append(self.apply_pallet(pygame.image.load(os.path.join(self.texture_path,"arm7.png")),self.pallet)) 
    def Draw(self):
        self.Animation(self)
    def collide(self,side="bottom"):
        collide = 0
        if side=="bottom":
            for i in range(0,self.hitbox.w):
                if not common.out_of_bounds((self.hitbox.x+i,self.hitbox.y+self.hitbox.h-1)):
                    if common.loaded_level.collision.get_at((self.hitbox.x+i,self.hitbox.y+self.hitbox.h-1))==1:
                        collide +=1
        elif side=="grounded":
            for i in range(0,self.hitbox.w):
                if not common.out_of_bounds((self.hitbox.x+i,self.hitbox.y+self.hitbox.h)):
                    if common.loaded_level.collision.get_at((self.hitbox.x+i,self.hitbox.y+self.hitbox.h))==1:
                        collide +=1
        elif side=="top":
            for i in range(0,self.hitbox.w):
                if not common.out_of_bounds((self.hitbox.x+i,self.hitbox.y)):
                    if common.loaded_level.collision.get_at((self.hitbox.x+i,self.hitbox.y))==1:
                        collide +=1
        elif side=="left":
            for i in range(1,self.hitbox.h-4):
                if not common.out_of_bounds((self.hitbox.x,self.hitbox.y+i)):
                    if common.loaded_level.collision.get_at((self.hitbox.x,self.hitbox.y+i))==1:
                        collide +=1
        elif side=="right":
            for i in range(1,self.hitbox.h-4):
                if not common.out_of_bounds((self.hitbox.x+self.hitbox.w-1,self.hitbox.y+i)):
                    if common.loaded_level.collision.get_at((self.hitbox.x+self.hitbox.w-1,self.hitbox.y+i))==1:
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
        elif self.x+self.x_vel+(self.hitbox.w/2)>common.loaded_level.collision_texture.get_width():
            self.x=common.loaded_level.collision_texture.get_width()-(self.hitbox.w/2)
            self.x_vel=0
        else:
            self.x += self.x_vel
        if self.y+self.y_vel-(self.hitbox.h/2)<0:
            self.y=self.hitbox.h/2
            self.y_vel=0
        elif self.y+self.y_vel+(self.hitbox.h/2)>common.loaded_level.collision_texture.get_height():
            self.y=common.loaded_level.collision_texture.get_height()-(self.hitbox.h/2)
            self.y_vel=0
        else:
            self.y += self.y_vel
        if self.x_vel<=0.01 and self.x_vel>=-0.01:
            self.x_vel = 0
        self.hitbox.x = self.x-self.texture_size[0]
        self.hitbox.y = self.y-self.texture_size[1]
        still_colliding = True
        ticker = common.Ticker(100)
        ticker.Trigger()
        while still_colliding:
            ticker.Tick()
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
                if self.x_vel<0:
                    self.x_vel=0
            elif not self.grounded:
                self.collisions["left"]=False
            if self.collide("right")>=2:
                self.collisions["right"]=True
                self.x-=1
                self.hitbox.x-=1
                still_colliding=True
                if self.x_vel>0:
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
            if not ticker.active:
                time.sleep(2)
                raise RuntimeError("collision hang at "+str((self.x,self.y)))
        w_offset = -constants.screen_scale/2
        h_offset = -constants.screen_scale
        pos = (int((self.x-common.loaded_level.camera[0])*constants.screen_scale+w_offset),int((self.y-common.loaded_level.camera[1])*constants.screen_scale+h_offset))
        angle = math.degrees(math.atan((pygame.mouse.get_pos()[1]-pos[1])/(int(pygame.mouse.get_pos()[0]-pos[0])+0.1)))
        if pos[0]<=pygame.mouse.get_pos()[0]:
            angle -=180
        angle+=180
        self.angle = angle
class TransitionObject():
    def __init__(self,rect,dest,dest_level):
        self.rect = rect
        self.dest = dest
        self.dest_level = dest_level
    def check(self):
        if self.rect.collidepoint((common.player.x,common.player.y)):
            common.loaded_level.load(self.dest_level)
            common.player.x = self.dest[0]
            common.player.y = self.dest[1]
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
        elif self.id==3:
            self.dest_id = 1
        else:
            raise ValueError("Invalid transition id: "+str(self.id))
    def check(self):
        if self.rect.collidepoint((common.player.x,common.player.y)):
            if self.id==0:
                try:
                    common.run.intermediary.levelarray[str((common.global_position[0],common.global_position[1]-2))].load()
                except KeyError:
                    common.loaded_level.load("test2")
                    print("No valid level could be loaded at "+str(common.global_position[0])+", "+str(common.global_position[1]-2)+", so the default level was loaded")
            elif self.id==1:
                try:
                    common.run.intermediary.levelarray[str((common.global_position[0]+2,common.global_position[1]))].load()          
                except KeyError:
                    common.loaded_level.load("test2")
                    print("No valid level could be loaded at "+str(common.global_position[0]+2)+", "+str(common.global_position[1])+", so the default level was loaded")
            elif self.id==2:
                try:
                    common.run.intermediary.levelarray[str((common.global_position[0],common.global_position[1]+2))].load()
                except KeyError:
                    common.level_level.load("test2")
                    print("No valid level could be loaded at "+str(common.global_position[0])+", "+str(common.global_position[1]+2)+", so the default level was loaded")
            elif self.id==3:
                try:
                    common.run.intermediary.levelarray[str((common.global_position[0]-2,common.global_position[1]))].load()
                except KeyError:
                    common.loaded_level.load("test2")
                    print("No valid level could be loaded at "+str(common.global_position[0]-2)+", "+str(common.global_position[1])+", so the default level was loaded")
            else:
                raise ValueError("Invalid transition id")
            if len(common.level_transitions)==0:
                raise ValueError("Destination level "+common.loaded_level.name+" has no valid entrance")
            for i in common.level_transitions:
                if type(i)==DynamicTransitionObject:
                    if i.id==self.dest_id:
                        common.player.x = i.dest[0]
                        common.player.y = i.dest[1]
def new_enemy(x,y,maxhp,type,xp=0):
    enemy = Entity(type,type,xp)
    enemy.x = x
    enemy.y = y
    enemy.max_hp = maxhp
    enemy.hp = maxhp
    if type=="mite":
        enemy.max_speed = constants.MAX_SPEED*1.4
    enemy.update_physics()
    if len(common.enemies)==0:
        common.enemies.append(enemy)
    else:
        for i in range(len(common.enemies)):
            if common.enemies[i]==None:
                enemy.index = i
                common.enemies[i] = enemy
                break
            elif i==len(common.enemies)-1:
                enemy.index = i+1
                common.enemies.append(enemy)