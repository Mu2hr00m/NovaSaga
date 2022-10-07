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
    def Trigger(self):
        if self.tick==-1:
            self.tick = 0
            self.active = True
    def Reset(self):
        self.tick = -1
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
def Font(color,rect=pygame.Rect,text=str):
    cur_pos = [rect.x,rect.y]
    base = small_font["scaled"].copy()
    if type(color)==str:
        color=constants.CHAR_COLORS.get(color)
    for i in base:
        arr = pygame.PixelArray(base[i])
        arr.replace((255,255,255),color)
        arr.close()
    for i in text:
        loaded_level.hud.blit(base.get(i,base["def"]),cur_pos)
        cur_pos[0]+=6*constants.screen_scale
Settings = None
Keybinds = None
enemies = []
projectiles = []
level_transitions = []
boxes = []
player = None
loaded_level = None
global_position = (0,0)
run = None
tick = 0
realclock = time.time()
small_font = {"origin":{},"scaled":{}}
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
    small_font["scaled"].update({i:pygame.transform.scale(small_font["origin"][i],(5*constants.screen_scale,7*constants.screen_scale))})
