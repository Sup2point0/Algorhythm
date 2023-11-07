'''
Implements the `Sprite` base class for sprite classes to derive from.

Unsafe to import.
'''

import pygame as py

from core import screen, sprites
import util


class Sprite(py.sprite.Sprite):
  '''Base class from which all game sprites derive, providing inherent attributes, functionality and utility.'''

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
    self.sx, self.sy = 0, 0
    self.align: tuple[int, int] = align or (0, 0)

    self.surf: py.Surface
    self.rect: py.Rect

  def show(self, layer: str):
    '''Add sprite to `sprites.active` to render in `layer`.'''

    sprites.active.add(self, layer = sprites.active.layer[layer])

  def position(self, shake = False):
    '''Update sprite `rect` position, adjusting for screen scroll, shake, and rotation (and maybe zoom in future).'''

    x = self.x
    y = self.y

    if shake:
      x -= screen.shake.x()
      y += screen.shake.y()
    if hasattr(self, "display"):
      if self.display.scroll:
        self.sy = util.slide(self.sy, self.display.scroll())
        y += self.sy

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
