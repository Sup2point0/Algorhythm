'''
Implements the `Cover` class for screen transitions.
'''

import pygame as pg

from core import screen, sprites
from innate.sprite import Sprite
import util


class Cover(Sprite):
  '''A screen cover to create fade transitions.'''

  def __init__(self, alpha = None, *, root = None):
    '''Create a screen cover.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `alpha` | `num`, `util.Alpha` | Alpha value of cover. If only a number is provided, the bounds will default to 0 and 255. |
    | `root` | `Callable` | Function replacing `self.update()`. |
    '''

    super().__init__(groups = [sprites.fade])

    self.alpha = alpha if isinstance(alpha, util.Alpha) else util.Alpha(alpha)
    self.root = root

    self.surf = pg.Surface(screen.size)
    self.surf.fill(pg.Color(0x000000ff))
    self.rect = self.surf.get_rect()

  def update(self):
    super().show("fade")
    self.root(self)
    self.surf.set_alpha(self.alpha.value)
