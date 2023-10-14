'''
Base sprite functionality
'''

import pygame as py

from core import screen, sprites


class Sprite(py.sprite.Sprite):
  '''Base class from which all game sprites derive, providing inherent attributes and utility.'''

  def __init__(self,
    pos = None,
    align = None,
    groups = list(),
  ):
    '''
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `pos` | `num, num` | Coordinates of position of sprite. |
    | `align` | `int, int` | Alignment of sprite in x and y directions, respectively. Can be `-1`, `0`, `1`. |
    | `groups` | `list[py.sprite.Group]` | Groups to add element to. |
    '''

    super().__init__(*groups)

    self.x, self.y = pos or screen.origin
    self.align: tuple[int, int] = align or (0, 0)

    self.surf: py.Surface
    self.rect: py.Rect

  def show(self, layer: str):
    '''Add sprite to `sprites.active` to render in `layer`.'''

    sprites.active.add(self, layer = sprites.active.layer[layer])

  def position(self):
    '''Update sprite `rect` position, adjusting for screen shake and rotation.'''

    x = self.x + screen.shake.x()
    y = self.y + screen.shake.y()
    lx, ly = self.align

    match lx:
      case -1:
        self.rect.left = x
      case 0:
        self.rect.centerx = x
      case 1:
        self.rect.right = x

    match ly:
      case -1:
        self.rect.top = y
      case 0:
        self.rect.centery = y
      case 1:
        self.rect.bottom = y

  @ property
  def image(self):
    return self.surf

  @ property
  def pos(self):
    '''Coordinates of element.'''

    return [self.x, self.y]