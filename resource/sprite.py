'''
Base sprite functionality
'''

import pygame as py

from core import screen


class Sprite(py.sprite.Sprite):
  '''Base class from which all game sprites derive, providing inherent attributes and utility.'''

  def __init__(self,
    pos = None,
    align = (0, 0),
    groups = None,
  ):
    '''
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `pos` | `num, num` | Position coordinates. |
    | `align` | `int, int` | Alignment of sprite... |
    | `groups` | `list[py.sprite.Group]` | Groups to add element to. |
    '''

    super().__init__(*groups)

    xy = pos or screen.origin
    self.x = xy[0]
    self.y = xy[1]
    self.align = align

    self.surf: py.Surface
    self.rect: py.Rect

  def shake(self):
    '''Adjust sprite position to screen shake.'''

    self.rect.x += screen.shake.x()
    self.rect.y += screen.shake.y()

  @ property
  def image(self):
    return self.surf

  @ property
  def pos(self):
    '''Coordinates of the element.'''

    return [self.x, self.y]
