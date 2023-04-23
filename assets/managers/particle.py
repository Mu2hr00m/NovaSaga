from assets.managers import common,constants
import pygame,random,math
class ParticleArea():
    def __init__(self,rect,freq,color,behavior,duration,variation):
        self.rect = rect
        self.freq = freq
        self.color = color
        self.uuid = "0-0-0-0"
        self.behavior = BehaviorMap[behavior]
        self.duration = duration
        self.variation = variation
    def spawn_particles(self):
        for i in range(self.rect.w):
            for j in range(self.rect.h):
                if random.random()<self.freq:
                    if self.variation>0:
                        duration = random.randint(self.duration-self.variation,self.duration+self.variation)
                    else:
                        duration = self.duration
                    common.NewThing(Dust([i+self.rect.x,j+self.rect.y],self.behavior,self.color,duration),common.newparticles)
class Dust():
    def __init__(self,pos,behavior,color,duration):
        self.pos = pos
        self.behavior = behavior
        if type(color)==dict:
            color = common.DynamicColor(pygame.Color(color["color1"][0],color["color1"][1],color["color1"][2]),pygame.Color(color["color2"][0],color["color2"][1],color["color2"][2]),color["color_index"],color["frequency"],color.get("alpha",False))
        self.color = color
        self.x_vel = 0
        self.y_vel = 0
        self.uuid = "0-0-0-0"
        self.duration = common.Ticker(duration)
        self.duration.Trigger()
    def kill(self):
        common.delparticles.append(self.uuid)
    def Draw(self):
        self.duration.Tick()
        self.behavior(self)
        if not self.duration.active:
            self.kill()
        if type(self.color)==common.DynamicColor:
            constants.layer_3.set_at((int(self.pos[0]),int(self.pos[1])),self.color.call())
        else:
            constants.layer_3.set_at((int(self.pos[0]),int(self.pos[1])),self.color)
def FallingDust(self):
    value = random.randint(0,9)
    if value<=2:
        self.pos[0]-=1
    elif value>=7:
        self.pos[0]+=1
    elif value==5:
        self.pos[1]+=1
def Spark(self):
    angle = random.random()*6.28-3.14
    if self.x_vel == 0:
        self.x_vel = math.sin(angle)
        self.y_vel = math.cos(angle)
    self.y_vel += constants.DEF_GRAVITY/2
    self.pos[0] += self.x_vel
    self.pos[1] += self.y_vel
BehaviorMap = {"FallingDust":FallingDust,"Spark":Spark}