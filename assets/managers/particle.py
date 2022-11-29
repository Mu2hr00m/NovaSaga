from assets.managers import common,constants
import pygame,random
def NewParticle(particle):
    if len(common.particles)==0:
        common.particles.append(particle)
    else:
        for i in range(len(common.particles)):
            if common.particles[i]==None:
                particle.index = i
                common.particles[i] = particle
                break
            elif i==len(common.particles)-1:
                particle.index = i+1
                common.particles.append(particle)
class ParticleArea():
    def __init__(self,rect,freq,color,behavior,duration,variation):
        self.rect = rect
        self.freq = freq
        self.color = color
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
                    NewParticle(Dust([i,j],self.behavior,self.color,duration))
class Dust():
    def __init__(self,pos,behavior,color,duration):
        self.pos = pos
        self.behavior = behavior
        if type(color)==dict:
            color = common.DynamicColor(pygame.Color(color["color1"][0],color["color1"][1],color["color1"][2]),pygame.Color(color["color2"][0],color["color2"][1],color["color2"][2]),color["color_index"],color["frequency"],color.get("alpha",False))
        self.color = color
        self.index = 0
        self.duration = common.Ticker(duration)
        self.duration.Trigger()
    def kill(self):
        common.particles[self.index] = None
    def draw(self):
        self.duration.Tick()
        self.behavior(self)
        if not self.duration.active:
            self.kill()
        if type(self.color)==common.DynamicColor:
            constants.WIN.set_at(self.pos,self.color.call())
        else:
            constants.WIN.set_at(self.pos,self.color)
def FallingDust(self):
    value = random.randint(0,9)
    if value<=2:
        self.pos[0]-=1
    elif value>=7:
        self.pos[0]+=1
    elif value==5:
        self.pos[1]+=1
BehaviorMap = {"FallingDust":FallingDust}