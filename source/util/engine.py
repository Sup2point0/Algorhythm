'''
Implements utility functions related to the game engine.
'''

import pygame as pg

from core import screen


def cord(x = 0.5, y = 0.5):
  '''Return coordinates normalised to screen size, where the screen centre is the origin.'''

  return (screen.cx * (x + 1), screen.cy * (y + 1))


def root(rect, x = None, y = None, *, align = (0, 0)):
  '''Return coordinates to place a rect at the given position (considering its size).
  
  | argument | type | description |
  | :------- | :--- | :---------- |
  | `rect` | `pygame.Rect` | The rect to position. |
  | `x`, `y` | `int`, `float` | Defaults to screen centre. |
  | `align` | `(int, int)` | X and Y alignment, respectively. `0` for centre, `1` for right and bottom, `-1` for left and top. |
  '''

  # Just some clever numerical manipulation that then becomes obfuscated. Sorry.
  return (
    (screen.cx if x is None else x) - rect.width * (align[0] + 1) / 2,
    (screen.cy if y is None else y) - rect.height * (align[1] + 1) / 2
  )


def slide(var, target, speed = 2):  # TODO change speed to decimal scalar
  '''Return variable altered partially towards target. Used for smooth motion.'''

  return var + (target - var) / speed
  # alt = (target - var) / speed
  # return (var + alt) if abs(alt) >= 0.5 else target


def resize(surf, size) -> pg.Surface:
  '''Resize a surface to a specific size, fitting in as much of the original surface as possible.

  | parameter | type | description |
  | :-------- | :--- | :---------- |
  | `surf` | `pygame.Surface` | Pygame surface to resize (generally an image asset). |
  | `size` | `num, num` | Dimensions to resize to. |
  '''

  iwidth, iheight = surf.get_size()
  nwidth, nheight = size

  if iwidth / iheight < nwidth / nheight:
    scale = nwidth / iwidth
  else:
    scale = nheight / iheight

  return pg.transform.scale_by(surf, scale)


def beatseq(start, stop, step):
  '''Generate a sequence of evenly spaced beats between `start` and `stop`.'''

  return (
    each * step for each in
    range(round(start / step), round(stop / step))
  )


def beats(start, count, step):
  '''Generate a sequence with length `count` of evenly spaced beats.'''

  return (start + i * step for i in range(count))
