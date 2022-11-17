import pygame,os,pathlib,json
from assets.managers import common
BLOCK_SIZE = 8
HALF_BLOCK_SIZE = int(BLOCK_SIZE * 0.5)
BLOCK_DIM = 8
BLOCK_SCALE = BLOCK_SIZE / BLOCK_DIM
BLOCK_WIDTH = 32
BLOCK_HEIGHT = 24
WIDTH, HEIGHT = BLOCK_SIZE * BLOCK_WIDTH, BLOCK_SIZE * BLOCK_HEIGHT
MAX_ZOOM = 20
MIN_ZOOM = 0.0625
screen_scale = 4
disp_win = pygame.display.set_mode((WIDTH*screen_scale,HEIGHT*screen_scale))
pygame.display.set_caption("Nova Saga Level Editor")
collision = pygame.Surface((1,1))
display = pygame.Surface((1,1))
hud = pygame.Surface((WIDTH*screen_scale,HEIGHT*screen_scale))
hud.set_colorkey((0,0,0))
zoom = 1.0
cam = [5,37]
keys = None
font = pygame.font.Font(None,8*screen_scale)
smallfont = pygame.font.Font(None,4*screen_scale)
key_cooldown = {}
colors = {"in_use":(0,1,0),0:(0,1,0),1:(0,1,0),2:(0,1,0),3:(0,1,0),4:(0,1,0),5:(0,1,0),6:(0,1,0),7:(0,1,0),8:(0,1,0),9:(0,1,0)}
layer = 1
leveldata = {}
def KeyCheck(key,boolean=True):
    if keys[key] and not key_cooldown[key].active and boolean:
        key_cooldown[key].Trigger()
        return True
    else:return False
def Bridge(args=None,args2=None):
    return args
def NotImplemented(args=None):
    print("Not Implemented")
    return args
def load_level(level_id):
    if level_id!=None:
        ui_assets["open_file"].isopen = False
        global collision
        global display
        global leveldata
        collision_file = pathlib.Path("assets","levels",level_id,"collision.png")
        display_file = pathlib.Path("assets","levels",level_id,"display.png")
        data_file = pathlib.Path("assets","levels",level_id,"data.json")
        if not data_file.exists():
            raise FileNotFoundError("Verify that the level "+level_id+" has a data.json file")
        leveldata = json.load(data_file.open())
        if not collision_file.exists() and not display_file.exists():
            raise FileNotFoundError("Verify that the level "+level_id+" has either a collision.png or a display.png")
        elif not collision_file.exists():
            collision = pygame.image.load(display_file)
            for j in range(collision.get_width()-1):
                for k in range(collision.get_height()-1):
                    if collision.get_at((j,k))!=(0,0,0,255):
                        collision.set_at((j,k),(0,0,0,0))
            display = pygame.image.load(display_file)
            display = pygame.transform.scale(display,(display.get_width()*leveldata.get("level_scale",1),display.get_height()*leveldata.get("level_scale",1)))
        elif not display_file.exists():
            display = pygame.image.load(collision_file)
            collision = pygame.image.load(collision_file)
            display = pygame.transform.scale(display,(display.get_width()*leveldata.get("level_scale",1),display.get_height()*leveldata.get("level_scale",1)))
        else:
            display = pygame.image.load(display_file)
            collision = pygame.image.load(collision_file)
        collision = pygame.transform.scale(collision,(display.get_width(),display.get_height()))
def list_levels():
    e=os.listdir(os.path.join("assets","levels"))
    levels = []
    for i in e:
        if pathlib.Path(os.path.join("assets","levels",i)).is_dir():levels.append(i)
    return levels
def dropdownMenu(items,rect):
    pos = [rect.x+rect.w/2,rect.y+rect.h]
    surfaces = []
    for i in items:
        surfaces.append(font.render(i,False,(0,1,0)))
    max_len = 0
    for i in surfaces:
        if i.get_width()>max_len:max_len=i.get_width()
    max_len += 4*screen_scale
    pos[0] -= max_len/2
    if pos[0]<=0:pos[0]=0
    pos = [pos[0]+2*screen_scale,pos[1]+2*screen_scale]
    clicked_rect = None
    for i in range(len(surfaces)):
        rect = pygame.Rect(pos[0],pos[1],max_len-4*screen_scale,surfaces[0].get_height()+screen_scale)
        if pygame.mouse.get_focused():
            if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()):
                clicked_rect = items[i]
        pos[1]+=surfaces[0].get_height()+screen_scale
    return clicked_rect
def draw_dropdownMenu(items,rect):
    pos = [rect.x+rect.w/2,rect.y+rect.h]
    surfaces = []
    for i in items:
        surfaces.append(font.render(i,False,(0,1,0)))
    max_len = 0
    for i in surfaces:
        if i.get_width()>max_len:max_len=i.get_width()
    max_len += 4*screen_scale
    pos[0] -= max_len/2
    if pos[0]<=0:pos[0]=0
    height = len(items)*surfaces[0].get_height()+4*screen_scale+(len(items)-1)*screen_scale
    pygame.draw.rect(hud,(0,128,128),pygame.Rect(pos[0],pos[1],max_len,height))
    pos = [pos[0]+2*screen_scale,pos[1]+2*screen_scale]
    for i in surfaces:
        rect = (pygame.Rect(pos[0],pos[1],max_len-4*screen_scale,surfaces[0].get_height()+screen_scale))
        if pygame.mouse.get_focused():
            if rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(hud,(64,255,255),rect)
                else:
                    pygame.draw.rect(hud,(32,160,160),rect)
        hud.blit(i,pos)
        pos[1]+=surfaces[0].get_height()+screen_scale
class UIElement():
    def __init__(self,name,path,pos):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image,(self.image.get_width()*screen_scale/2,self.image.get_height()*screen_scale/2))
        self.rect = pygame.Rect(pos[0]*screen_scale,pos[1]*screen_scale,self.image.get_width(),self.image.get_height())
        self.name = name
        self.isopen = False
        self.gather = None
        self.type = None
        self.action = None
        self.drawer = None
    def draw(self):
        hud.blit(self.image,self.rect)
        if self.isopen:
            if self.drawer!=None and self.gather!=None:
                self.drawer(self.gather(),self.rect)
    def check(self):
        if pygame.mouse.get_focused():
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()) and not key_cooldown["mouse1"].active:
                key_cooldown["mouse1"].Trigger()
                self.isopen = not self.isopen
        if self.isopen:
            if self.type!=None and self.action!=None and self.gather!=None:
                self.action(self.type(self.gather(),self.rect))
class dynamicLevelTransition():
    def __init__(self,rect,style,id,dest_pos):
        self.rect = rect
        self.style = style
        self.id = id
        self.dest_pos = dest_pos
    def draw(self):
        pygame.draw.rect(hud,(128,128,128),self.rect)
ui_assets = {}
ui_runners = {"open_file":[list_levels,dropdownMenu,draw_dropdownMenu,load_level,(2,2)],"save_file":[NotImplemented,Bridge,Bridge,Bridge,(18,2)]}
for i in os.listdir("level-creator-assets"):
    j = pathlib.Path(os.path.join("level-creator-assets",i))
    if j.is_file():
        if j.suffix==".png":
            l=j.stem.replace("-","_")
            k=ui_runners[l]
            ui_assets.update({l:UIElement(l,j,k[4])})
            ui_assets[l].gather = k[0]
            ui_assets[l].type = k[1]
            ui_assets[l].drawer = k[2]
            ui_assets[l].action = k[3]
def draw():
    global collision
    global display
    global hud
    global leveldata
    disp_win.fill((128,128,128))
    hud.fill((0,0,0,0))
    hud.blit(font.render(str(zoom),False,(255,255,255)),(30,30))
    pygame.draw.rect(hud,(70,70,70),pygame.Rect(0,0,disp_win.get_width(),18*screen_scale))
    pygame.draw.rect(hud,(50,50,50),pygame.Rect(0,0,disp_win.get_width(),18*screen_scale),screen_scale)
    for i in leveldata.get("level_transitions",range(1)):
        if type(i)!=int:pass
    for i in ui_assets:
        ui_assets[i].draw()
    collision.set_alpha(255)
    display.set_alpha(255)
    if layer==1:
        collision.set_alpha(128)
        disp_win.blit(pygame.transform.scale(collision,(collision.get_width()*zoom,collision.get_height()*zoom)),(cam[0]*screen_scale,cam[1]*screen_scale))
        disp_win.blit(pygame.transform.scale(display,(display.get_width()*zoom,display.get_height()*zoom)),(cam[0]*screen_scale,cam[1]*screen_scale))
    elif layer==2:
        display.set_alpha(128)
        disp_win.blit(pygame.transform.scale(display,(display.get_width()*zoom,display.get_height()*zoom)),(cam[0]*screen_scale,cam[1]*screen_scale))
        disp_win.blit(pygame.transform.scale(collision,(collision.get_width()*zoom,collision.get_height()*zoom)),(cam[0]*screen_scale,cam[1]*screen_scale))
    disp_win.blit(hud,(0,0))
    pygame.display.update()
def main():
    clock = pygame.time.Clock()
    isRunning = True
    print("level creator ready")
    global keys
    global zoom
    global key_cooldown
    t = ["abcdefghijklmnopqrstuvwxyz0123456789","MINUS","EQUALS","PERIOD","SPACE"]
    for i in t[0]:
        t.append(i)
    del t[0]
    for i in t:
        print(str((i,eval("pygame.K_"+i))))
    e = pygame.key.get_pressed()
    keys = {}
    for i in enumerate(e):keys.update({i[0]:i[1]})
    for i in range(len(keys)):key_cooldown.update({i:common.Ticker(6)})
    keys.update({"mouse1":False,"mouse2":False})
    key_cooldown.update({"mouse1":common.Ticker(6)})
    for i in key_cooldown.keys():
        if keys.get(i,None)==None:print(i)
    while isRunning:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                break
        pygame.event.clear()
        for i in enumerate(pygame.key.get_pressed()):keys[i[0]]=i[1]
        for i in key_cooldown:
            key_cooldown[i].SafeTick()
            if not keys[i]:key_cooldown[i].Reset()
        if KeyCheck(pygame.K_EQUALS,zoom<MAX_ZOOM):
            if zoom>=1:zoom+=1
            else:zoom*=2
        if KeyCheck(pygame.K_MINUS,zoom>MIN_ZOOM):
            if zoom>=2:zoom-=1
            else:zoom/=2
        if keys[pygame.K_w]:cam[1]+=1
        if keys[pygame.K_a]:cam[0]+=1
        if keys[pygame.K_s]:cam[1]-=1
        if keys[pygame.K_d]:cam[0]-=1
        if KeyCheck(pygame.K_o):ui_assets["open_file"].isopen=not ui_assets["open_file"].isopen
        for i in ui_assets.values():i.check()
        draw()
        pygame.event.clear()
    pygame.quit()
if __name__ == "__main__":
    main()