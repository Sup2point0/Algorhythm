Algorhythm Code


# TODO
= update modules to directly import innate for general use
= update sprite classes to use super(self, Object).__init__()


@ level.py
class Track:
  def __init__():
    self.dur = ...


@ sprite.py
class Sprite:
  def position(self, shake = False):
    '''Update sprite `rect` position, adjusting for screen scroll, shake, and rotation (and maybe zoom in future).'''

    x = self.x
    y = self.y + screen.shake.y()

    if shake:
      x -= screen.shake.x()
      y += screen.shake.y()
    if self.display.scroll:
      y += self.display.scroll()

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


@ innate/__init__.py
'''
This package implements several fundamental classes for widespread use throughout the game.
'''

from innate.value import BoundValue as Val
from innate.object import Object


@ core.py
class game:
  select = {
    "track": None,
    "difficulty": None,
    "sort": "default",
    "inverse": True,
  }

class screen:
  scroll = {
    "select": Val(),
    **{
      f"select.{each}": Val()
      for each in levels.levels
    },
    "settings": Val(),
    "settings.sounds": Val(),
  }

class sprites:
  splash["select.tracks"] = []

class ui:
  class size:
    class select:
      series = [, ]
      track = [, ]

class config:
  sorts = [
    ("default", None),
    ("score", lambda each: each.),  # TODO
    ("name", lambda each: each.track.name),
    ("artist", lambda each: each.track.artist),
    ("duration", lambda each: each.track.dur),
    # NOTE brackets needed around lambda?
  ]

class opt:
  class col:
    accent = [64, 144, 241, 255]


@ main.py
from splash import splash, live

def control():
  splash.live.run()


@ util.py
def asset(file) -> py.Surface:
  '''Load an image file to a pygame Surface.'''

  return py.image.load(f"assets.{file}").convert()

def log(**attrs):
  '''Adds the specified attributes to a given function. Used as a decorator.'''

  def wrapper(func):
    def root(*args, **kwargs):
      func(*args, **kwargs)

    for each in attrs:
      root.__setattr__(each, attrs[each])

    return root

  return wrapper


@ roots.py
def select(var, state):
  '''Change `var` in `game.select` to `state`.'''

  def root():
    game.select[var] = state

  return root


class state:
  def flip(var):
    '''...'''

    def root():
      var() = not var()

    return root

  def switch(var):
    '''...'''

    def root(state):
      var() = state

    return root
