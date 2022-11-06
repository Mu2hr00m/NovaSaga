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
    def __init__(self,rect,freq,color,behavior,duration):
        self.rect = rect
        self.freq = freq
        self.color = color
        self.behavior = BehaviorMap[behavior]
        self.duration = duration
    def spawn_particles(self):
        for i in range(self.rect.w):
            for j in range(self.rect.h):
                if random.random()<self.freq:
                    NewParticle(Dust([i,j],self.behavior,(192,128,255),40))
class Dust():
    def __init__(self,pos,behavior,color,duration):
        self.pos = pos
        self.behavior = behavior
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
        constants.WIN.set_at(self.pos,self.color)
def FallingDust(self):
    value = random.randint(0,3)
    if value==0:
        self.pos[0]-=1
    elif value==1:
        self.pos[0]+=1
    else:
        self.pos[1]+=1
BehaviorMap = {"FallingDust":FallingDust}