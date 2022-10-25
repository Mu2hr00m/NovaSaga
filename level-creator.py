from asyncio import constants
from dis import dis
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
colors = {"in_use":(0,1,0)}
layer = 1
leveldata = {}
class UIElement():
    def __init__(self,name,path,pos):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image,(self.image.get_width()*screen_scale/2,self.image.get_height()*screen_scale/2))
        self.rect = pygame.Rect(pos[0]*screen_scale,pos[1]*screen_scale,self.image.get_width(),self.image.get_height())
        self.name = name
        self.isopen = False
    def draw(self):
        hud.blit(self.image,self.rect)
ui_assets = {}
for i in os.listdir("level-creator-assets"):
    j = pathlib.Path(os.path.join("level-creator-assets",i))
    if j.is_file():
        if j.suffix==".png":
            ui_assets.update({j.stem.replace("-","_"):UIElement(j.stem.replace("-","_"),j,(8,8))})
def draw():
    global collision
    global display
    global hud
    global leveldata
    disp_win.fill((128,128,128))
    hud.fill((0,0,0,0))
    hud.blit(font.render(str(zoom),False,(255,255,255)),(30,30))
    pygame.draw.rect(hud,(70,70,70),pygame.Rect(0,0,disp_win.get_width(),16*screen_scale))
    pygame.draw.rect(hud,(50,50,50),pygame.Rect(0,0,disp_win.get_width(),16*screen_scale),screen_scale)
    for i in ui_assets.values():
        i.draw()
    if ui_assets["open_file"].isopen:
        e = os.listdir(os.path.join("assets","levels"))
        levels = []
        for i in e:
            if pathlib.Path(os.path.join("assets","levels",i)).is_dir():
                levels.append(i)
        lines = 0
        for i in levels:
            surface = font.render(i,False,(0,1,0))
            hud.blit(surface,(25*screen_scale,5*screen_scale+8*screen_scale*lines))
            rect = surface.get_rect()
            rect.x = 25*screen_scale
            rect.y = 5*screen_scale+8*screen_scale*lines
            if pygame.mouse.get_focused() and rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                collision_file = pathlib.Path("assets","levels",i,"collision.png")
                display_file = pathlib.Path("assets","levels",i,"display.png")
                data_file = pathlib.Path("assets","levels",i,"data.json")
                if not data_file.exists():
                    raise FileNotFoundError("Verify that the level "+i+" has a data.json file")
                leveldata = json.load(data_file.open())
                if not collision_file.exists() and not display_file.exists():
                    raise FileNotFoundError("Verify that the level "+i+" has either a collision.png or a display.png")
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
            lines+=1
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
    keys = pygame.key.get_pressed()
    for i in range(len(keys)):
        key_cooldown.update({i:common.Ticker(6)})
    key_cooldown[pygame.K_o].threshold = 60
    while isRunning:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                break
        pygame.event.clear()
        keys = pygame.key.get_pressed()
        for i in key_cooldown:
            key_cooldown[i].Tick()
        if keys[pygame.K_EQUALS] and not key_cooldown[pygame.K_EQUALS].active and zoom<MAX_ZOOM:
            key_cooldown[pygame.K_EQUALS].Trigger()
            if zoom>=1:
                zoom+=1
            else:
                zoom*=2
        if keys[pygame.K_MINUS] and not key_cooldown[pygame.K_MINUS].active and zoom>MIN_ZOOM:
            key_cooldown[pygame.K_MINUS].Trigger()
            if zoom>=2:
                zoom-=1
            else:
                zoom/=2
        if keys[pygame.K_w]:
            cam[1]+=1
        if keys[pygame.K_a]:
            cam[0]+=1
        if keys[pygame.K_s]:
            cam[1]-=1
        if keys[pygame.K_d]:
            cam[0]-=1
        if keys[pygame.K_o] and not key_cooldown[pygame.K_o].active:
            key_cooldown[pygame.K_o].Trigger()
            ui_assets["open_file"].isopen=not ui_assets["open_file"].isopen
        draw()
        pygame.event.clear()
    pygame.quit()
if __name__ == "__main__":
    main()