'''
Screen transition cover
'''

import pygame as py

from core import screen, sprites, config


class Cover(py.sprite.Sprite):
  '''A screen cover to create fade transitions.'''

  def __init__(self, alpha = 0, *, root = None, bounds = None):
    '''Create a screen cover.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `alpha` | `num` | Starting alpha value of cover. |
    | `root` | `Callable` | Function replacing `self.update()`. |
    | `bounds` | `[int, int]` | Lower and upper bounds of alpha value. |
    '''

    super().__init__(sprites.fade)
    
    self.root = root
    self.bounds = bounds or (0, 255)

    self.surf = py.Surface(screen.size, py.SRCALPHA)
    py.draw.rect(
      surface = self.surf,
      color = py.Color(0x000000ff),
      rect = py.Rect(0, 0, *screen.size),
    )
    self.alpha = alpha
    self.rect = self.surf.get_rect()

  def update(self):
    self.root(self)

  @ property
  def alpha(self):
    return self.surf.get_alpha()
  
  @ alpha.setter
  def alpha(self, value):
    self.surf.set_alpha(
      self.bounds[1] if value > self.bounds[1] else
      self.bounds[0] if value < self.bounds[0] else
      value
    )
