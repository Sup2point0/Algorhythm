'''
Hitline
'''

import pygame as pg

from core import level, screen, sprites, config
from innate.sprite import Sprite
import util


class Hitline(Sprite):
  '''The hitline.'''

  def __init__(self):
    '''Create a hitline.'''

    super().__init__(
      pos = [screen.cx, screen.y - config.lane.space * 4],
      groups = [sprites.lines]
    )

    self.size = [0, 5]

  def update(self):
    super().show("hitline")

    if level.tick > 30:
      self.size[0] = util.slide(self.size[0], screen.x, 10)
    
    self.surf = pg.Surface(self.size)
    self.surf.fill(0xffffff)
    self.rect = self.surf.get_rect()

    super().position()
