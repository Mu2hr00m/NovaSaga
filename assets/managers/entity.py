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
        if self.name!="nova":
            if common.delentities.count(self.uuid)==0:
                common.delentities.append(self.uuid)
        else:
            print("game over") #this will eventually trigger game over cutscene, right now it fixes a crash
    def damage(self,amount=1):
        if (self.iframes.active,self.invulnerable)==(False,False):
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
        self.invulnerable = False
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
        self.uuid = "0-0-0-0"
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
            self.Animation = animation.mite_anim
            self.max_speed = constants.MAX_SPEED*0.8
            self.animation_ticks.threshold = 10
            self.name = "mite"
        if AItype=="dangle_wire":
            self.AIpointer = ai.no_physics
            self.Animation = animation.dangling_wire_anim
            self.animation_ticks.threshold = math.pi
            self.hitbox = pygame.Rect(0,0,0,0)
            self.pull_strength = 0
            self.deviation = 0
            self.name = "None"
        for i in os.listdir(constants.PORTRAIT_PATH):
            item = i.split("-",1)
            if item[0]==self.name:
                self.portraits.update({item[1].split(".",1)[0]:pygame.transform.scale(pygame.image.load(os.path.join(constants.PORTRAIT_PATH,i)),(32*constants.screen_scale,32*constants.screen_scale))})
        #print(self.portraits)
        self.overlay_active = False
        self.xp = xp
        self.overlay = common.loaded_level.camera_surface.copy()
        self.overlay = pygame.transform.scale(self.overlay,(self.overlay.get_width()*3,self.overlay.get_height()*3))
        self.overlay.set_alpha(96)
        self.overlay.fill((0,0,0))
        pygame.draw.circle(self.overlay,(24,24,24),(self.overlay.get_width()/2,self.overlay.get_height()/2),96)
        pygame.draw.circle(self.overlay,(40,40,40),(self.overlay.get_width()/2,self.overlay.get_height()/2),64)
        pygame.draw.circle(self.overlay,(64,64,64),(self.overlay.get_width()/2,self.overlay.get_height()/2),32)
        if self.name!="None":
            self.spritesheet = common.Spritesheet(os.path.join("assets","sprites",texturepath+"_sprites.png"))
            self.palletized_sprites = []
            self.pallet = 0
            for i in self.spritesheet["pallets"]:
                if i!=self.spritesheet["pallets"][0]:
                    data = {}
                    for j in self.spritesheet.keys():
                        if type(j)==int:
                            data2 = {"offset":self.spritesheet[j]["offset"]}
                            for k in self.spritesheet[j]:
                                if isinstance(self.spritesheet[j][k],pygame.Surface):
                                    data2.update({k:self.apply_pallet(self.spritesheet[j][k],i,self.spritesheet["pallets"][0])})
                            data.update({j:data2})
                    self.palletized_sprites.append(data)
        #print(self.palletized_sprites[0])
        if self.ai_type=="player":
            self.text_color = constants.CHAR_COLORS["nova"]
            self.animation_ticks.threshold = 35
            self.inventory = {"main_1":None,"main_2":None,"main_3":None,"cursor":None}
            self.portraits.update({"happy":pygame.transform.scale(pygame.image.load(os.path.join(constants.PORTRAIT_PATH,"nova-happy.png")),(32*constants.screen_scale,32*constants.screen_scale))})
            self.portraits.update({"neutral":pygame.transform.scale(pygame.image.load(os.path.join(constants.PORTRAIT_PATH,"nova-neutral.png")),(32*constants.screen_scale,32*constants.screen_scale))})
            self.portraits.update({"sad":pygame.transform.scale(pygame.image.load(os.path.join(constants.PORTRAIT_PATH,"nova-sad.png")),(32*constants.screen_scale,32*constants.screen_scale))})
            for i in range(constants.INV_WIDTH*constants.INV_HEIGHT):
                self.inventory.update({"inv_"+str(i):None})
            self.facing_away = False 
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
        if self.hitbox.w==0 and self.hitbox.h==0:
            return None
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
    def __init__(self,rect,id,dest,global_pos):
        self.rect = rect
        self.id = id
        self.dest = dest
        self.global_pos = global_pos
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
            level_transitions = []
            for i in common.newentities.values():
                if type(i)==DynamicTransitionObject:
                    level_transitions.append(i)
            if len(level_transitions)==0:
                raise ValueError("Destination level "+common.loaded_level.name+" has no valid entrance")
            for i in level_transitions:
                if i.id==self.dest_id:
                    common.player.x = i.dest[0]
                    common.player.y = i.dest[1]
def new_entity(x,y,maxhp,type,xp=0):
    entity = Entity(type,type,xp)
    entity.x = x
    entity.y = y
    entity.max_hp = maxhp
    entity.hp = maxhp
    entity.update_physics()
    common.NewThing(entity)