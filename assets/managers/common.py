from assets.managers import constants
import pygame,time,os,pathlib,json,random,uuid
class Placeholder():
    def __init__(self,attrs):
        for i in attrs:
            exec("self."+i+" = None")
loaded_level = Placeholder(["hud"])
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
    def SafeTick(self,amount=1):
        if self.tick>=0 and self.tick<self.threshold:
            self.tick+=amount
            if self.tick<0:
                self.tick = 0
            if self.tick>self.threshold:
                self.tick = self.threshold
    def Loop(self,amount=1):
        if self.tick>=0:
            self.tick+=amount
        if self.tick>=self.threshold:
            self.tick = 0
    def Reflect(self,amount=1):
        if self.tick>-1:
            if self.active:
                self.tick+=amount
                if self.tick>self.threshold:
                    self.tick = self.threshold
                    self.active = False
            else:
                self.tick-=amount
                if self.tick<0:
                    self.tick = 0
                    self.active = True
    def Trigger(self):
        if self.tick==-1:
            self.tick = 0
            self.active = True
    def Reset(self):
        self.tick = -1
        self.active = False
    def __repr__(self):
        if self.active:return "Ticker with threshold of {0} and tick at {1} and is active".format(self.threshold,self.tick)
        return "Ticker with threshold of {0} and tick at {1} and is inactive".format(self.threshold,self.tick)
def Scale(surface:pygame.Surface,factor:float=constants.screen_scale)->pygame.Surface:
    return pygame.transform.scale(surface,(surface.get_width()*factor,surface.get_height()*factor))
def GetPressed(control)->bool:
    Key = Keybinds[control]
    if type(Key)==str:
        if pygame.mouse.get_focused():
            if Key=="lclick":
                return PressedKeysNoCooldown["mouse1"]
            elif Key=="rclick":
                return PressedKeysNoCooldown["mouse2"]
            else:
                return PressedKeysNoCooldown[Key]
    else:
        return PressedKeysNoCooldown[Key]
def ExceptionPrinter(exception:Exception):
    exceptionType = str(type(exception))
    exceptionType = exceptionType.split("\'")[1]
    exceptionModule = str(exception.__traceback__.tb_frame).split("\'")[1]
    print("exception of type {0} caught on line {1} in file {2}: {3}".format(exceptionType,exception.__traceback__.tb_lineno,exceptionModule,exception))
class DynamicColor():
    def __init__(self,color1:pygame.Color,color2:pygame.Color,color_index:int,frequency:int,include_alpha=False):
        self.color1 = color1
        self.color2 = color2
        self.index = color_index
        self.frequency = frequency
        self.alpha = include_alpha
        self.previous_color = self.color1.lerp(self.color2,0.5)
        self.ticker = Ticker(frequency)
        self.ticker.Trigger()
    def call(self):
        if self.index==0:
            self.previous_color = self.color1.lerp(self.color2,random.random())
        elif self.index==1:
            self.ticker.Reflect()
            self.previous_color = self.color1.lerp(self.color2,self.ticker.tick/self.ticker.threshold)
        elif self.index==2:
            if self.ticker.tick<self.ticker.threshold/3:
                self.ticker.SafeTick(random.randint(-3,5))
            elif self.ticker.tick>self.ticker.threshold/3*2:
                self.ticker.SafeTick(random.randint(-5,3))
            else:
                self.ticker.SafeTick(random.randint(-4,4))
            self.previous_color = self.color1.lerp(self.color2,self.ticker.tick/self.ticker.threshold)
        return self.previous_color
    def copy(self):
        return DynamicColor(self.color1,self.color2,self.index,self.frequency,self.alpha)
def KeyDirect(key)->bool:
    return PressedKeys[key]
def ReloadSettings():
    file = None
    truefile = None
    global Settings
    global Keybinds
    if not os.path.exists("settings"):
        truefile = open("settings","x")
        truefile.close()
        truefile = pathlib.Path("settings")
        truefile.write_text(json.dumps(constants.DEF_SETTINGS,indent=4))
    else:
        truefile = pathlib.Path("settings")
    file = json.loads(truefile.read_text())
    Settings = file
    if file.get("keybindings",0)==0:
        file.update({"keybindings":constants.DEFKEYBINDS})
        truefile.write_text(json.dumps(file,indent=4))
        Keybinds = constants.DEFKEYBINDS
    else:
        Keybinds = file["keybindings"]
    if __name__=="__constants__":
        pygame.quit()
def out_of_bounds(pos,safety = 0):
    oob = False
    if pos[0]<safety or pos[0]>constants.layer_1.get_width()-1-safety:
        oob = True
    if pos[1]<safety or pos[1]>constants.layer_1.get_height()-1-safety:
        oob = True
    return oob
def Font(color,rect=pygame.Rect,text=str,size=1,dest_surface=constants.layer_5):
    return_surface = False
    if type(dest_surface)!=pygame.Surface:
        dest_surface=pygame.Surface((rect.w,rect.h))
        dest_surface.set_colorkey((0,0,0))
        return_surface=True
    cur_pos = [rect.x,rect.y]
    base = small_font["scaled_"+str(size)].copy()
    for i in base:
        base[i]=base[i].copy()
    if type(color)==str:
        color=constants.CHAR_COLORS.get(color,constants.CHAR_COLORS["default"])
    for i in base:
        arr = pygame.PixelArray(base[i])
        arr.replace((255,255,255),color)
        arr.close()
    for i in range(len(text)-1):
        if text[i]=="\n":
            cur_pos[1]+=9*constants.screen_scale/2*size
            cur_pos[0]=rect.x
        elif text[i]=="^":
            if i+3<=len(text):
                cur_pos[0]+=2*constants.screen_scale/2*size
                if text[i+1]=="k":
                    dest_surface.blit(key_img["scaled_"+str(size)][text[i+2]],(cur_pos[0],cur_pos[1]-constants.screen_scale/2*size))
                elif text[i+1]=="m":
                    dest_surface.blit(key_img["scaled_"+str(size)]["M_"+text[i+2]],(cur_pos[0],cur_pos[1]-constants.screen_scale/2*size))
                cur_pos[0]+=12*constants.screen_scale/2*size
                i+=2
        else:
            if i==0:
                dest_surface.blit(base.get(text[i],base["def"]),cur_pos)
                cur_pos[0]+=6*constants.screen_scale/2*size
            elif i==1:
                if text[i-1]!="^":
                    dest_surface.blit(base.get(text[i],base["def"]),cur_pos)
                    cur_pos[0]+=6*constants.screen_scale/2*size
            else:
                if text[i-1]!="^" and text[i-2]!="^":
                    dest_surface.blit(base.get(text[i],base["def"]),cur_pos)
                    cur_pos[0]+=6*constants.screen_scale/2*size
    if return_surface:
        return dest_surface
def Spritesheet(path:str):
    spritesheet = pygame.image.load(path)
    #spritesheet.set_colorkey((0,0,0,0))
    pixel_1 = spritesheet.get_at((0,0))
    num_rows = pixel_1.r      #red channel of top left most pixel tells how many rows
    pallet_len = pixel_1.g    #green channel of top left most pixel tells how many pixels long a given pallet is
    num_pallets = pixel_1.b   #blue channel of top left most pixel tells how many pallets, arranged right to left
    data = {"pallets":[],"origin":spritesheet}
    for i in range(num_pallets):
        data["pallets"].append(pygame.Surface((pallet_len,1)))
        data["pallets"][i].blit(spritesheet.subsurface(pygame.Rect(-pallet_len+spritesheet.get_width()-pallet_len*i,0,pallet_len,1)),(0,0))
    row_index = 1
    for i in range(num_rows):
        row_data = {}
        pixel_2 = spritesheet.get_at((i*2+1,0))   #pixel 2: red channel is sprite width, green is sprite height, blue is sprite count
        pixel_3 = spritesheet.get_at((i*2+2,0))   #pixel 3: red channel is offset x, green is offset y
        pixel_3 = [pixel_3.r,pixel_3.g,pixel_3.b] #if offset is greater than 128, the difference from it to 255 is the offset, but negative
        sprite_rect = pygame.Rect(0,row_index,pixel_2.r,pixel_2.g)
        if pixel_3[0]>128:
            pixel_3[0] = pixel_3[0]-255
        if pixel_3[1]>128:
            pixel_3[1] = pixel_3[1]-255
        row_data.update({"offset":(pixel_3[0],pixel_3[1])})
        for j in range(pixel_2.b):
            row_data.update({j:pygame.Surface((pallet_len,1))})
            row_data[j] = spritesheet.subsurface(sprite_rect)
            sprite_rect.x+=pixel_2.r
        data.update({i:row_data})
        row_index+=pixel_2.g
    return data
entities = {}
boxes = {}
particles = {}
newentities = {}
newparticles = {}
delentities = []
delparticles = []
SoundLibrary = {}
MusicLibrary = {}
Entity,Dust,ParticleArea,Bullet,DynamicLevelTransition,Level = None,None,None,None,None,None
def NewThing(thing,dest:dict=newentities):
    thing.uuid = str(uuid.uuid4())
    dest.update({thing.uuid:thing})
Settings = None
Keybinds = None
active_text = None
current_map = ""
player = None
backgrounds = []
e=None
global_position = (0,0)
run = None
frametime_total = 0
frametime_draw = 0
frametime_draw_reads = [0,0,0,0,0,0,0,0,0,0]
frametime_draw_pos = Ticker(9)
frametime_physics = 0
fps = 0
sharp_fps = 0
PressedKeys = constants.keyboard_binds.copy()
PressedKeys.update({"mouse1":False,"mouse2":False,"mouse3":False,"mouse4":False,"mouse5":False})
KeyCooldown = PressedKeys.copy()
PressedKeysNoCooldown = PressedKeys.copy()
for i in KeyCooldown:
    KeyCooldown[i] = Ticker(constants.DEF_KEY_COOLDOWN)
realclock = time.time()
small_font = {"origin":{},"scaled_1":{},"scaled_2":{},"scaled_3":{}}
key_img = {"origin":{},"scaled_1":{},"scaled_2":{},"scaled_3":{}}
font_data = Spritesheet("assets/managers/font.png")
menu = "main"
text = "abcdefghijklmnopqrstuvwxyz0123456789_*\\:,%.?\";/~-!()[]{}#+= "
k=0
for i in font_data.values():
    if type(i)==dict:
        for j in i.values():
            if type(j)==pygame.Surface:
                try:
                    small_font["origin"].update({text[k]:j})
                except IndexError:
                    small_font["origin"].update({"def":j})
                k+=1
for i in small_font["origin"]:
    small_font["scaled_1"].update({i:pygame.transform.scale(small_font["origin"][i],(5*constants.screen_scale/2,7*constants.screen_scale/2))})
    small_font["scaled_2"].update({i:pygame.transform.scale(small_font["origin"][i],(5*constants.screen_scale,7*constants.screen_scale))})
    small_font["scaled_3"].update({i:pygame.transform.scale(small_font["origin"][i],(5*constants.screen_scale*1.5,7*constants.screen_scale*1.5))})
base = small_font["origin"].copy()
for i in small_font["origin"]:
    surface = pygame.Surface((9,9))
    surface.fill((128,128,128))
    pygame.draw.rect(surface,(0,1,0),pygame.Rect(0,0,9,9),1)
    base[i]=base[i].copy()
    arr = pygame.PixelArray(base[i])
    arr.replace((255,255,255),(64,64,64))
    arr.close()
    surface.blit(base[i],(2,1))
    key_img["origin"].update({i:surface})
key_img["origin"].update({"M_0":pygame.image.load(os.path.join(constants.FONT_PATH,"l_click.png"))})
key_img["origin"].update({"M_1":pygame.image.load(os.path.join(constants.FONT_PATH,"r_click.png"))})
key_img["origin"].update({"M_2":pygame.image.load(os.path.join(constants.FONT_PATH,"m_click.png"))})
key_img["origin"].update({"M_3":pygame.image.load(os.path.join(constants.FONT_PATH,"mouse_4.png"))})
key_img["origin"].update({"M_4":pygame.image.load(os.path.join(constants.FONT_PATH,"mouse_5.png"))})
for i in key_img["origin"]:
    key_img["scaled_1"].update({i:pygame.transform.scale(key_img["origin"][i],(9*constants.screen_scale*0.5,9*constants.screen_scale*0.5))})
    key_img["scaled_2"].update({i:pygame.transform.scale(key_img["origin"][i],(9*constants.screen_scale,9*constants.screen_scale))})
    key_img["scaled_3"].update({i:pygame.transform.scale(key_img["origin"][i],(9*constants.screen_scale*1.5,9*constants.screen_scale*1.5))})