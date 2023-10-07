'''
Utility classes and functions
'''

import random
import json
import colorsys

from core import screen, sprites, config, opt


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
  '''Functions involving finding.'''

  def row(key) -> str:
    '''Find which row of the keyboard a key belongs to.'''

    rows = config.keys.__dict__
    for row in rows:
      if key in rows[row]:
        return row
    else:
      return "spec"

  def col(key):
    '''Find suitable colour for a game key.'''
    
    return vars(opt.col)[find.row(key)]


class interpolate:
  '''Functions involving interpolation.'''

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


class Alpha:
  '''An alpha value, restricted to a certain range.
  
  The value should be altered with `self.alt` to avoid going outside the bounds.
  '''

  def __init__(self, value = 255, bounds = (0, 255)):
    '''Create an alpha value.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `value` | `num` | Starting alpha value. |
    | `bounds` | `num, num` | Lower and upper bounds of alpha value. |
    '''

    self.value = value
    self.bounds = bounds
    self._check_()
  
  def _check_(self):
    '''Internal method to ensure alpha value is within bounds.'''

    if self.value < min(self.bounds):
      self.value = min(self.bounds)
    elif self.value > max(self.bounds):
      self.value = max(self.bounds)

  def alt(self, value):
    '''Alter alpha value.'''

    if value is True:
      self.value = 255
    elif value is False:
      self.value = 0
    else:
      self.value += value
    self._check_()

    return self.value

  def bounded(self):
    '''Check if alpha value is at bound.'''

    return self.value in self.bounds
