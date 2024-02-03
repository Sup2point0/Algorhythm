'''
Implements the `Sprite` base class for sprite classes to derive from.

Unsafe to import.
'''

import pygame as pg

from core import screen, sprites
import util


class Sprite(pg.sprite.Sprite):
  '''Base class from which all game sprites derive, providing inherent attributes, functionality and utility.'''

  class Draggable:
    '''Settings for allowing a sprite to be dragged by the mouse.'''

    def __init__(self,
      dir = "xy",
      x = None,
      y = None,
      lock = None,
    ):
      '''Create a drag setting.

      | parameter | type | description |
      | :-------- | :--- | :---------- |
      | dir | str "xy", "x", "y" | Direction(s) which sprite can be dragged in. |
      '''

      self.dir = dir
      self.lock = lock

      class lx:
        lower, upper = x
      class ly:
        lower, upper = y

      self.lx = lx
      self.ly = ly

  ###
  def __init__(self,
    pos = None,
    align = None,
    drag = None,
    groups = list(),
  ):
    '''
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `pos` | `num, num` | Coordinates of position of sprite. |
    | `align` | `int, int` | Alignment of sprite in x and y directions, respectively. Can be `-1`, `0`, `1`. |
    | `drag` | `innate.Sprite.Draggable` | Drag settings for sprite. |
    | `groups` | `list[pg.sprite.Group]` | Groups to add element to. |
    '''

    super().__init__(*groups)

    self.x, self.y = pos or screen.origin
    self.sx, self.sy = 0, 0
    self.align = align or (0, 0)
    self.drag = drag

    self.surf: pg.Surface
    self.rect: pg.Rect

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
    if getattr(self, "display", None):
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

  def dragged(self):
    '''Handle sprite being dragged.'''

    if not self.drag:
      return
    if self.drag.lock():
      return

    pos = pg.mouse.get_pos()

    if "x" in self.drag.dir:
      self.x = util.restrict(pos[0], bounds = self.drag.lx)
    if "y" in self.drag.dir:
      self.y = util.restrict(pos[1], bounds = self.drag.ly)

  @ property
  def image(self):
    return self.surf

  @ property
  def pos(self):
    '''Coordinates of element.'''

    return [self.x, self.y]
