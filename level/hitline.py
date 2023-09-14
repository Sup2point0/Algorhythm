'''
Hitline
'''

import pygame as py

from core import level, screen, sprites, config
import util


class Hitline(py.sprite.Sprite):
  '''The hitline.'''

  def __init__(self):
    '''Create a hitline.'''

    super().__init__(sprites.lines)

    self.pos = [screen.cx, screen.y - config.lanespace * 4]
    self.size = [2, 5]

  def update(self):
    sprites.active.add(self, layer = sprites.active.layer["hitline"])

    if level.tick > 30:
      self.size[0] = util.slide(self.size[0], screen.x, 10)
    
    self.image = py.Surface(self.size)
    self.image.fill(0xffffff)
    self.rect = self.image.get_rect()
    self.rect.topleft = util.root(self.rect, y = self.pos[1])
