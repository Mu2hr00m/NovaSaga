from assets.managers import constants
import pygame,time,os,pathlib,json
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
    def Loop(self,amount=1):
        if self.tick>=0:
            self.tick+=amount
        if self.tick>=self.threshold:
            self.tick = 0
    def Trigger(self):
        if self.tick==-1:
            self.tick = 0
            self.active = True
    def Reset(self):
        self.tick = -1
        self.active = False
def GetPressed(control):
    Key = Keybinds[control]
    if type(Key)==str:
        if pygame.mouse.get_focused():
            if Key=="lclick":
                return pygame.mouse.get_pressed(5)[0]
            elif Key=="rclick":
                return pygame.mouse.get_pressed(5)[1]
    else:
        return pygame.key.get_pressed()[Key]
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
def out_of_bounds(pos):
    oob = False
    if pos[0]<0 or pos[0]>constants.WIN.get_width()-1:
        oob = True
    if pos[1]<0 or pos[1]>constants.WIN.get_height()-1:
        oob = True
    return oob
def Font(color,rect=pygame.Rect,text=str,size=1):
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
                    loaded_level.hud.blit(key_img["scaled_"+str(size)][text[i+2]],(cur_pos[0],cur_pos[1]-constants.screen_scale/2*size))
                elif text[i+1]=="m":
                    loaded_level.hud.blit(key_img["scaled_"+str(size)]["M_"+text[i+2]],(cur_pos[0],cur_pos[1]-constants.screen_scale/2*size))
                cur_pos[0]+=12*constants.screen_scale/2*size
                i+=2
        else:
            if i==0:
                loaded_level.hud.blit(base.get(text[i],base["def"]),cur_pos)
                cur_pos[0]+=6*constants.screen_scale/2*size
            elif i==1:
                if text[i-1]!="^":
                    loaded_level.hud.blit(base.get(text[i],base["def"]),cur_pos)
                    cur_pos[0]+=6*constants.screen_scale/2*size
            else:
                if text[i-1]!="^" and text[i-2]!="^":
                    loaded_level.hud.blit(base.get(text[i],base["def"]),cur_pos)
                    cur_pos[0]+=6*constants.screen_scale/2*size
Settings = None
Keybinds = None
enemies = []
projectiles = []
level_transitions = []
boxes = []
particles = []
particle_spawners = []
active_text = None
player = None
loaded_level = None
e=None
global_position = (0,0)
run = None
tick = 0
realclock = time.time()
small_font = {"origin":{},"scaled_1":{},"scaled_2":{},"scaled_3":{}}
key_img = {"origin":{},"scaled_1":{},"scaled_2":{},"scaled_3":{}}
menu = "main"
text = "abcdefghijklmnopqrstuvwxyz0123456789_!()[]{}#+-=~"
for i in text:
    small_font["origin"].update({i:pygame.image.load(os.path.join(constants.FONT_PATH,i+".png"))})
small_font["origin"].update({" ":pygame.image.load(os.path.join(constants.FONT_PATH,"_space_.png"))})
small_font["origin"].update({".":pygame.image.load(os.path.join(constants.FONT_PATH,"_period_.png"))})
small_font["origin"].update({"*":pygame.image.load(os.path.join(constants.FONT_PATH,"_asterisk_.png"))})
small_font["origin"].update({"/":pygame.image.load(os.path.join(constants.FONT_PATH,"_slash_.png"))})
small_font["origin"].update({"\\":pygame.image.load(os.path.join(constants.FONT_PATH,"_backslash_.png"))})
small_font["origin"].update({"%":pygame.image.load(os.path.join(constants.FONT_PATH,"_percent_.png"))})
small_font["origin"].update({":":pygame.image.load(os.path.join(constants.FONT_PATH,"_colon_.png"))})
small_font["origin"].update({";":pygame.image.load(os.path.join(constants.FONT_PATH,"_semicolon_.png"))})
small_font["origin"].update({",":pygame.image.load(os.path.join(constants.FONT_PATH,"_comma_.png"))})
small_font["origin"].update({"?":pygame.image.load(os.path.join(constants.FONT_PATH,"_question_.png"))})
small_font["origin"].update({"\"":pygame.image.load(os.path.join(constants.FONT_PATH,"_quotes_.png"))})
small_font["origin"].update({"def":pygame.image.load(os.path.join(constants.FONT_PATH,"_unknown_.png"))})
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