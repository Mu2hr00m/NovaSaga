from assets.managers import common,constants
import os,pygame

class TextElement():
    def __init__(self,text,speaker,emotion,requires_button=True,form=0,speed=12):
        self.text = text
        self.speaker = speaker
        self.emotion = emotion
        self.button = requires_button
        self.form = form
        self.speed = 1/speed
        if speed!=None:
            self.ticker = common.Ticker(int(len(text)*(constants.FPS*self.speed)))
        self.emotion_ticker = common.Ticker(constants.FPS)
        self.ticker.Trigger()
        self.rect = pygame.Rect(0,0,0,0)
        if form==0:
            self.rect = pygame.Rect(constants.screen_scale*32,constants.screen_scale*192-constants.screen_scale*32,constants.screen_scale*256-constants.screen_scale*32,constants.screen_scale*32)
        elif form==1:
            self.rect = pygame.Rect(0,constants.screen_scale*192-constants.screen_scale*32,constants.screen_scale*256,constants.screen_scale*32)
        elif form==2:
            self.rect = pygame.Rect(constants.screen_scale*80,constants.screen_scale*80,constants.screen_scale*96,constants.screen_scale*32)
        elif form==3:
            self.rect = pygame.Rect(constants.screen_scale*80,constants.screen_scale*90,constants.screen_scale*96,constants.screen_scale*12)
    def draw(self):
        text = ""
        if self.speed!=None:
            index = int(self.ticker.tick/self.ticker.threshold*len(self.text))
            for i in range(index):
                text = text+self.text[i]
        else:
            text=self.text
        common.Font(self.speaker,pygame.Rect(self.rect.x+constants.screen_scale*2,self.rect.y+constants.screen_scale*2,self.rect.w-4*constants.screen_scale,self.rect.h-4*constants.screen_scale),text.lower(),2)
        self.ticker.SafeTick()
class TextSequence():
    def __init__(self,text):
        self.text = text
        self.elements = {}
        tick = 0
        for i in self.text:
            if type(i)==TextElement:
                self.elements.update({tick:i})
                tick+=i.ticker.threshold
            elif type(i)==int:
                tick+=i
        self.ticker = common.Ticker(tick)
        self.ticker.Trigger()
    def update(self):
        for i in self.elements:
            if i<=self.ticker.tick:
                self.elements[i].draw()
        self.ticker.SafeTick()
    def close(self):
        for i in self.elements:
            self.elements[i].ticker.tick = 0
        self.ticker.tick = 0
e = TextSequence([TextElement("hello world","nova",0),-60,TextElement("            e","",0,speed=36)])
