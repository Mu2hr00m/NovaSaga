import pygame
import os,random
random.seed(os.urandom(4))
pygame.font.init()
BLOCK_SIZE = 8
HALF_BLOCK_SIZE = int(BLOCK_SIZE * 0.5)
BLOCK_DIM = 8
BLOCK_SCALE = BLOCK_SIZE / BLOCK_DIM
BLOCK_WIDTH = 32
BLOCK_HEIGHT = 24
CAM_WIDTH = BLOCK_WIDTH * BLOCK_SIZE
CAM_HEIGHT = BLOCK_HEIGHT * BLOCK_SIZE
WIDTH, HEIGHT = BLOCK_SIZE * BLOCK_WIDTH, BLOCK_SIZE * BLOCK_HEIGHT
INV_WIDTH, INV_HEIGHT = 5,2
screen_scale = 4
DEF_FONT = pygame.font.Font(None, 5*screen_scale)
DEF_GRAVITY = 0.12
DEF_GROUND_DRAG = 0.8
DEF_AIR_DRAG = 0.95
MAX_FALL = 3
DEF_ACCEL = 0.14
DEF_AIR_ACCEL = 0.06
DEF_JUMP = 3
MAX_SPEED = 1
MAX_RECT_SIZE = 1024
FPS = 60
DEF_HP = 20
BUTTONSIZE = 12*screen_scale
ITEM_PATH = os.path.join("assets","sprites","items")
PROJ_PATH = os.path.join("assets","sprites","projectile")
ui_path = os.path.join("assets","managers","menu_ui")
disp_win = pygame.display.set_mode((WIDTH*screen_scale,HEIGHT*screen_scale),depth=32)
title_subtitles = ["Nova Saga: ","Mirror Worlds","The Unknown","Brain Games","The Game","LLOORREE!!!","Inspired by FTL","Inspired by Terraria","All Inclusive!","Indie Game!","Inspired by 20 Minutes till Dawn","Multiverse Theory","Quantum Mechanics","Uploading to human.exe","Not an Asteroid","Not Mind Controlling You"]
pygame.display.set_caption(title_subtitles[0]+title_subtitles[random.randint(1,len(title_subtitles)-1)])
if pygame.display.get_caption()[0]=="Nova Saga: All Inclusive!":
    pygame.display.set_icon(pygame.image.load(os.path.join(ui_path,"rainbow-icon.png")))
else:
    pygame.display.set_icon(pygame.image.load(os.path.join(ui_path,"icon.png")))
valid_text = ["qwertyuiopasdfghjklzxcvbnm1234567890","AMPERSAND","ASTERISK","AT","BACKQUOTE","BACKSLASH","BACKSPACE","CAPSLOCK","CLEAR","COLON","COMMA","CURRENCYUNIT","DELETE","DOLLAR","DOWN","END","EQUALS","ESCAPE","EXCLAIM","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","GREATER","HASH","HELP","HOME","INSERT","KP0","KP1","KP2","KP3","KP4","KP5","KP6","KP7","KP8","KP9","KP_0","KP_1","KP_2","KP_3","KP_4","KP_5","KP_6","KP_7","KP_8","KP_9","KP_DIVIDE","KP_ENTER","KP_EQUALS","KP_MINUS","KP_MULTIPLY","KP_PERIOD","KP_PLUS","LALT","LCTRL","LEFT","LEFTBRACKET","LESS","LSHIFT","MENU","MINUS","MODE","PAGEDOWN","PAGEUP","PAUSE","PERCENT","PERIOD","PLUS","POWER","QUESTION","QUOTE","RALT","RCTRL","RETURN","RIGHT","RIGHTBRACKET","RSHIFT","SEMICOLON","SLASH","SPACE","TAB","UNDERSCORE"]
keyboard_binds = {}
for i in valid_text[0]:valid_text.append(i)
del valid_text[0]
for i in range(255):
    if pygame.key.name(i)!="":
        keyboard_binds.update({i:False})
del valid_text
layer_0 = pygame.Surface((WIDTH,HEIGHT),depth=32) #background
layer_1 = pygame.Surface((WIDTH,HEIGHT),depth=32) #level background
layer_2 = pygame.Surface((WIDTH,HEIGHT),depth=32) #entities
layer_3 = pygame.Surface((WIDTH,HEIGHT),depth=32) #level foreground
layer_4 = pygame.Surface((WIDTH,HEIGHT),depth=32) #dynamic shadows
layer_4_a = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA,depth=32) #dynamic shadows afterdraw
layer_5 = pygame.Surface((WIDTH*screen_scale,HEIGHT*screen_scale),pygame.SRCALPHA,depth=32) #hud
layer_1.set_colorkey((0,0,0,255))
layer_2.set_colorkey((0,0,0,255))
layer_3.set_colorkey((0,0,0,255))
layer_4.set_colorkey((0,0,0,255))
#layer_4_a.set_colorkey((0,0,0,255))
#menu_surface = disp_win.copy()
#menu_surface.set_colorkey((0,0,0,0))
DEF_LEVEL = "test_display.png"
DEF_START_POS = (10 * BLOCK_SIZE, int(19.5 * BLOCK_SIZE))
PLAYER_VEL = 2
MAP_BACKGROUND_COLOR = (64,64,64)
START_TILE_COLOR = (128,0,192)
MEMORY_TILE_COLOR = (0,64,192)
DREAM_TILE_COLOR = (192,64,192)
LABYRINTH_TILE_COLOR = (128,128,128)
FRACTURE_TILE_COLOR = (128,128,255)
ABSTRACT_TILE_COLOR = (255,255,255)
ABYSS_TILE_COLOR = (128,0,0)
TRAUMA_TILE_COLOR = (255,0,0)
AWAKENING_TILE_COLOR = (128,255,128)
AURIC_DOOR_TILE_COLOR = (64,255,0)
SECRET_ROOM_TILE_COLOR = (255,128,0)
DEF_KEY_COOLDOWN = 10
PATH_TILE_COLOR = (0,1,0)
DEFKEYBINDS = {"left":pygame.K_a,"right":pygame.K_d,"jump":pygame.K_w,"action1":"lclick","action2":"rclick","action3":pygame.K_q,"inventory":pygame.K_e,"interact":pygame.K_SPACE}
DEF_SETTINGS = {"keybinds":DEFKEYBINDS}
FONT_PATH = os.path.join("assets","managers","font")
PORTRAIT_PATH = os.path.join("assets","sprites","profile")
CHAR_COLORS = {"default":(128,128,128),"nova":(192,128,255)}
CHAR_COLORS.setdefault("default",(128,128,128))
TEXTBOX_BACKGROUND = (32,32,32)
TEXTBOX_BORDER = (96,96,96)
MUSIC_END_EVENT = pygame.event.custom_type()