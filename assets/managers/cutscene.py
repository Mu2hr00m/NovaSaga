from assets.managers import common,constants,entity
import os,pygame,pathlib

class TextElement():
    def __init__(self,text,speaker,emotion,speed=12,size=1):
        self.owner = None
        self.text = text+" "
        self.speaker = speaker
        self.emotion = emotion
        self.color = speaker
        self.size = size
        self.portrait = None
        if speed!=None:
            self.speed = 1/speed
        else:
            self.speed = None
        text_len = 0
        if speed!=None:
            for i in self.text:
                if i!=" ":
                    text_len+=constants.FPS*self.speed
                elif i=="^":
                    text_len-=constants.FPS*self.speed*2
        self.ticker = common.Ticker(int(text_len))
        self.emotion_ticker = common.Ticker(constants.FPS)
        self.ticker.Trigger()
        if type(speaker)==entity.Entity:
            self.color = speaker.text_color
            self.portrait = speaker.portraits.get(self.emotion,speaker.portraits["default"])
    def draw(self):
        rect = self.owner.rect
        text = ""
        if type(self.speaker)==entity.Entity and self.owner.form==0:
            pos = [self.speaker.x,self.speaker.y-self.speaker.hitbox.h/2-15]
            pos[0] = int(int((pos[0]-common.loaded_level.camera[0])/constants.CAM_WIDTH*constants.disp_win.get_width()/constants.screen_scale)*constants.screen_scale)
            pos[1] = int(int((pos[1]-common.loaded_level.camera[1])/constants.CAM_WIDTH*constants.disp_win.get_width()/constants.screen_scale)*constants.screen_scale)
            rect = pygame.Rect(pos[0]-(rect.w/2),pos[1],rect.w,rect.h)
        if self.owner.form==1 and self.portrait!=None:
            common.loaded_level.hud.blit(self.portrait,(0,constants.screen_scale*192-constants.screen_scale*32))
        else:
            common.loaded_level.hud.blit(common.player.portraits["default"],(0,constants.screen_scale*192-constants.screen_scale*32))
        if self.speed!=None:
            index = int(self.ticker.tick/self.ticker.threshold*len(self.text))
            for i in range(index):
                text = text+self.text[i]
        else:
            text=self.text
        common.Font(self.color,pygame.Rect(rect.x+constants.screen_scale*2,rect.y+constants.screen_scale*2,rect.w-4*constants.screen_scale,rect.h-4*constants.screen_scale),text.lower(),self.size)
        self.ticker.SafeTick()
class TextSequence():
    def __init__(self,text,form=0,button=True,size=1,rect=pygame.Rect(0,0,0,0)):
        self.text = text
        self.form = form
        self.button = button
        self.size = size
        self.rect = rect
        self.is_open = False
        self.elements = {}
        tick = 0
        for i in self.text:
            if type(i)==TextElement:
                self.elements.update({tick:i})
                tick+=i.ticker.threshold
            elif type(i)==int:
                tick+=i
        for i in self.elements:
            self.elements[i].owner = self
            self.elements[i].size = self.size
        self.ticker = common.Ticker(tick)
        self.ticker.Trigger()
        if form==0:
            self.rect = rect
        elif form==1:
            self.rect = pygame.Rect(constants.screen_scale*32,constants.screen_scale*192-constants.screen_scale*32,constants.screen_scale*256-constants.screen_scale*32,constants.screen_scale*32)
        elif form==2:
            self.rect = pygame.Rect(0,constants.screen_scale*192-constants.screen_scale*32,constants.screen_scale*256,constants.screen_scale*32)
        elif form==3:
            self.rect = pygame.Rect(constants.screen_scale*80,constants.screen_scale*80,constants.screen_scale*96,constants.screen_scale*32)
        elif form==4:
            self.rect = pygame.Rect(constants.screen_scale*80,constants.screen_scale*90,constants.screen_scale*96,constants.screen_scale*12)
    def update(self):
        if common.GetPressed("interact") and self.ticker.tick==self.ticker.threshold:
            self.close()
        elif self.is_open:
            if self.form==1:
                pygame.draw.rect(common.loaded_level.hud,constants.TEXTBOX_BACKGROUND,pygame.Rect(constants.screen_scale*32,constants.screen_scale*192-constants.screen_scale*32,constants.screen_scale*256-constants.screen_scale*32,constants.screen_scale*32))
                pygame.draw.rect(common.loaded_level.hud,constants.TEXTBOX_BORDER,pygame.Rect(constants.screen_scale*32,constants.screen_scale*192-constants.screen_scale*32,constants.screen_scale*256-constants.screen_scale*32,constants.screen_scale*32),constants.screen_scale)
            for i in self.elements:
                if i<=self.ticker.tick:
                    self.elements[i].draw()
        self.ticker.SafeTick()
    def close(self):
        common.active_text = None
        self.is_open = False
        for i in self.elements:
            self.elements[i].ticker.tick = 0
        self.ticker.tick = 0
