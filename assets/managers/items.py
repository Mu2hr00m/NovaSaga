import pygame
from assets.managers import constants
from assets.managers import game_classes
from assets.managers import projectile
import random
def basic(self):
    spread = random.randint(-2,2)
    if not self.cooldown.active:
        self.cooldown.Trigger()
        projectile.new_projectile(projectile.Bullet(game_classes.player.x,game_classes.player.y,game_classes.player.angle+spread,"bullet.png",10,1,0,3))
items = []
items.append(game_classes.Item("basic","gun","gun.png",basic,game_classes.Ticker(30)))
game_classes.player.inventory.append(items[0])