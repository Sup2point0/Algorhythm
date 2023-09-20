'''
Screen transition cover
'''

import pygame as py

from core import screen, sprites
from resource.sprite import Sprite
import util


class Cover(Sprite):
  '''A screen cover to create fade transitions.'''

  def __init__(self, alpha = None, *, root = None):
    '''Create a screen cover.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `alpha` | `num`, `util.Alpha` | Alpha value of cover. If a number is provided, a default `util.Alpha` value is used with the number as the initial value. |
    | `root` | `Callable` | Function replacing `self.update()`. |
    '''

    super().__init__(groups = [sprites.fade])

    self.alpha = alpha if isinstance(alpha, util.Alpha) else util.Alpha(alpha)
    self.root = root

    self.surf = py.Surface(screen.size, py.SRCALPHA)
    py.draw.rect(
      surface = self.surf,
      color = py.Color(0x000000ff),
      rect = py.Rect(0, 0, *screen.size),
    )
    self.rect = self.surf.get_rect()

  def update(self):
    self.root(self)
    self.surf.set_alpha(self.alpha.value)
