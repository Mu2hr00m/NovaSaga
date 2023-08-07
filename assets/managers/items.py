import pygame,math
from assets.managers import constants
from assets.managers import projectile,common
import random,os
class Item():
    def __init__(self,id,type,texture,on_use,cooldown):
        self.id = id
        self.type = type
        self.cooldown = cooldown
        self.spritesheet = common.Spritesheet(os.path.join(constants.ITEM_PATH,texture))
        self.texture = self.spritesheet[0][0]
        self.inv_texture = common.Scale(self.spritesheet[1][0])
        self.on_use = on_use
    def __repr__(self):
        return "Item with id {0} and type {0}".format(self.id,self.type)
def basic(self):
    spread = random.randint(-2,2)
    if not self.cooldown.active:
        self.cooldown.Trigger()
        common.NewThing(projectile.Bullet(common.player.x,common.player.y,common.player.angle+spread,"bullet.png",10,1,0,3),common.newentities)
def gun2(self):
    spread = random.randint(-7,7)
    if not self.cooldown.active:
        self.cooldown.Trigger()
        common.NewThing(projectile.Bullet(common.player.x,common.player.y,common.player.angle+spread,"bullet.png",3,1,0,3),common.newentities)
def flashlight(self):
    common.player.editable_overlay.fill((0,0,0,0))
    common.player.editable_overlay.blit(common.player.overlay,(0,0))
    x1 = int(common.player.x-common.loaded_level.camera[0]+(192*(math.sin(common.player.angle-20))/math.pi))+constants.CAM_WIDTH/2
    y1 = int(common.player.x-common.loaded_level.camera[1]+(192*(math.cos(common.player.angle-20))/math.pi))+constants.CAM_HEIGHT/2
    x2 = int(common.player.x-common.loaded_level.camera[0]+(192*(math.sin(common.player.angle+20))/math.pi))+constants.CAM_WIDTH/2
    y2 = int(common.player.x-common.loaded_level.camera[1]+(192*(math.cos(common.player.angle+20))/math.pi))+constants.CAM_HEIGHT/2
    print((x1,y1,x2,y2))
    pygame.draw.polygon(common.player.editable_overlay,(1,1,1,0),((common.player.x-common.loaded_level.camera[0],common.player.x-common.loaded_level.camera[1]),(x1,y1),(x2,y2)))
items = {}
items.update({"gun":Item(basic,"gun","gun.png",basic,common.Ticker(30))})
items.update({"gun2":Item(gun2,"gun","gun.png",gun2,common.Ticker(40))})
items.update({"flashlight":Item(flashlight,"utility","gun.png",flashlight,common.Ticker(0))})