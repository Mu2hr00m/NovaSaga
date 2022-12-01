import pygame
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
def basic(self):
    spread = random.randint(-2,2)
    if not self.cooldown.active:
        self.cooldown.Trigger()
        projectile.new_projectile(projectile.Bullet(common.player.x,common.player.y,common.player.angle+spread,"bullet.png",10,1,0,3))
def gun2(self):
    spread = random.randint(-7,7)
    if not self.cooldown.active:
        self.cooldown.Trigger()
        projectile.new_projectile(projectile.Bullet(common.player.x,common.player.y,common.player.angle+spread,"bullet.png",3,1,0,3))
items = {}
items.update({"gun":Item(basic,"gun","gun.png",basic,common.Ticker(30))})
items.update({"gun2":Item(gun2,"gun","gun.png",gun2,common.Ticker(40))})