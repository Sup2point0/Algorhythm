'''
Implements various utility functions and classes used throughout the game modules.
'''

import random
import json
import colorsys

import pygame as py

from core import screen, sprites, config, opt
from innate import Val


## generic
def has(iterable, *values, every = True) -> bool:
  '''Check if `iterable` contains any of `values`.
  
  If `every` is `True`, it must contain every specified value.
  '''

  out = (each in iterable for each in values)
  return all(out) if every else any(out)
  
def index(iterable, *values, check = False) -> int | tuple[int, any] | None:
  '''Find index of first occurence of any value within `values`.

  If `check` is True, a tuple containing which value was found is returned instead.
  
  Returns `None` if no occurrences are found.
  '''

  # Some slightly questionable logical flow, but this helps to avoid needless iteration.
  for i, each in enumerate(iterable):
    if each in values:
      if check:
        for value in values:
          if value == each:
            return (i, value)
      else:
        return i
  
  return None

def log(**attrs):
  '''Adds the specified attributes to a given function. Used as a decorator.'''

  def wrapper(func):
    def root(*args, **kwargs):
      func(*args, **kwargs)

    for each in attrs:
      root.__setattr__(each, attrs[each])

    return root

  return wrapper


## engine
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

def slide(var, target, speed = 2):
  '''Return variable altered partially towards target. Used for smooth motion.'''

  return var + (target - var) / speed
  # alt = (target - var) / speed
  # return (var + alt) if abs(alt) >= 0.5 else target

def resize(surf, size) -> py.Surface:
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

  return py.transform.scale_by(root.surf, scale)

def overwrite(file, content: str):
  '''Overwrite a JSON file with `content`.'''

  file.seek(0)
  file.write(json.dumps(content))
  file.truncate()


## niche
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
    return has((lane.key for lane in sprites.lanes), key, every = False)
  
  if rows is None:
    keys = [key for key in config.keys.rand.keys() if not taken(key)]
  else:
    keys = [
      key for row in rows
      for key in vars(config.keys)[row].keys()
      if not taken(key)
    ]
  
  return random.choice(keys)


class find:
  def row(key) -> str:
    '''Find which row of the keyboard a key belongs to.'''

    rows = config.keys.__dict__
    for each in rows:
      if not each.startswith("_"):
        if key in rows[each]:
          return each
    else:
      return "spec"

  def col(key):
    '''Find suitable colour for a game key.'''
    
    return vars(opt.col)[find.row(key)]
  
  def asset(*files) -> py.Surface:
    '''Load an image file to a pygame Surface.'''

    for file in files:
      try:
        return py.image.load(f"assets/{file}")
      except:
        pass


class interpolate:
  def value(start, stop, percent: float):
    '''Interpolate any value between 2 endpoints.'''

    return start + percent * (stop - start)
  
  def col(start, stop, percent: float = 0.5):
    '''Interpolate between 2 colours. Alpha is not taken into account.'''

    lower = colorsys.rgb_to_hsv(*start[:3])
    upper = colorsys.rgb_to_hsv(*stop[:3])

    return colorsys.hsv_to_rgb(
      lower[0] + percent * (upper[0] - lower[0]),
      lower[1] + percent * (upper[1] - lower[1]),
      lower[2] + percent * (upper[2] - lower[2]),
    )


class Alpha(Val):
  '''A `BoundValue` representing an alpha value, with bounds defaulting to 0 and 255.'''

  def __init__(self, value, bounds = (0, 255)):
    '''Create an alpha value with the specified bounds.'''

    super().__init__(value, *bounds)

  def __call__(self):
    val = super().__call__()

    # ensure alpha values are safe to use
    if val < 0:
      val = 0
    elif val > 255:
      val = 255
    
    return val
