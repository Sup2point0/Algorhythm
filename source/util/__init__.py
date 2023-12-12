'''
Implements various utility functions and classes used throughout the game modules.
'''

# NOTE pending removal
import random
import json

import pygame as pg

from core import screen, sprites, config
##

import util.find
import util.lerp


## generic
def has(iterable, *values, every = False) -> bool:
  '''Check if `iterable` contains any of `values`.
  
  If `every` is `True`, it must contain every specified value.
  '''

  out = (each in iterable for each in values)
  return all(out) if every else any(out)


## calculations
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


## internal
def log(**attrs):
  '''Adds the specified attributes to a given function. Used as a decorator.'''

  def wrapper(func):
    def root(*args, **kwargs):
      func(*args, **kwargs)

    for each in attrs:
      root.__setattr__(each, attrs[each])

    return root

  return wrapper

def overwrite(file, content: str):
  '''Overwrite a JSON file with `content`.'''

  file.seek(0)
  file.write(json.dumps(content))
  file.truncate()


## niche
def beats(start, stop, step):
  '''Generate a sequence of evenly spaced beats.'''

  div = 1 / step
  return (
    each / div for each in
    range(round(start * div), round(stop * div))
  )

def setscore(score, digits: int = None) -> str:
  '''Add zeroes to the front of a value such that it is `digits` long.'''

  points = str(score)
  places = len(points)
  if digits is None:
    digits = len(str(config.score.apex))

  return (f"{'0' * (digits - places)}{score}") if places < digits else points

def randkey(rows: list[str] = None):
  '''Randomly select a key from the non-special game keys.
  
  The row(s) from which the key is selected can be restricted by specifying `rows`.
  '''
  
  def taken(key):
    return has((lane.key for lane in sprites.lanes), key)
  
  if rows is None:
    keys = [key for key in config.keys.rand.keys() if not taken(key)]
  else:
    keys = [
      key for row in rows
      for key in vars(config.keys)[row].keys()
      if not taken(key)
    ]
  
  return random.choice(keys)
