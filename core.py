'''
Global variables and constants for all modules to access.
'''

import pygame as py

# This module is imported by almost every file. As such,
# it should avoid importing any others, otherwise... CIRCULAR IMPORTS!
# These are exceptions, since they are safe to import.
from innate.value import BoundValue as Val
from innate.innate import Difficulty, Rank
from effects.shake import Shake


## globals
class game:
  '''Game-wide variables.'''

  version = "0.0.0"

  state = True
  '''
  | value | description |
  | :---- | :---------- |
  | `True` | Game is running. |
  | `False` | Game is paused. |
  | `int` | Game is unpausing. |
  | `None` | Game should be closed. |
  '''

  player = None
  level = None

  select = {
    "track": None,
    "difficulty": None,
    "sort": "default",
    "reverse": True,
  }

  events = []  # tracks events in frame
  keys = []  # tracks current pressed keys
  pulse = py.time.Clock()  # game timer

  series = ["tutorials", "origins", "protos", "decode", "special"]


class level:
  '''Level-specific variables.'''

  chart = None
  data = []
  
  beat = 0
  tick = 0

  score = 0
  scored = 0  # displayed score
  hits = 0
  perfect = 0
  chain = 0  # combo
  apex = 0  # max combo

  class lane:
    width = 0
    space = 0


class screen:
  '''Variables relating to the screen.
  
  `screen.state` and `screen.fade` control what displays on screen. Sprites only render if the current `screen.state` is in their configured list of screen states.
  
  When `screen.switch` is set, `screen.state` is updated to that at the start of the next frame (to avoid conflicting screen state processing within the same frame). While fading out, `screen.fade` becomes `'out'`, freezing sprites from updating. Once the screen entirely blacks out, `screen.fade` briefly becomes `'dark'`. In this time window (where the player cannot see anything), sprites update again, changing the rendered screen.
  '''

  x = 1280
  y = 720
  cx = x / 2
  cy = y / 2
  size = [x, y]
  origin = [cx, cy]

  switch = None
  state = None
  states = {
    "start", "select",
    *{f"select.{each}" for each in game.series},
    "environ", "environ.load", "environ.create",
    "settings", "settings.sounds", "settings.visuals",
    "account",
    "play", "score",
  }
  
  fade = None
  '''
  | value | description |
  | :---- | :---------- |
  | `None` | No fading animation. |
  | `out` | Fading out to dark. |
  | `dark` | Screen is entirely black – safe to switch screens. |
  | `in` | Fading in from black. |
  '''

  scroll = {
    "select": Val(0),
    **{
      f"select.{each}": Val(0)
      for each in game.series
    },
    "settings": Val(0),
    "settings.sounds": Val(0),
  }

  track = []

  class shake:
    x = Shake()
    y = Shake()


class sprites:
  '''Sprite groups.'''

  fade = py.sprite.Group()
  pause = py.sprite.Group()

  lines = py.sprite.Group()
  lanes = py.sprite.Group()
  notes = py.sprite.Group()
  effects = py.sprite.Group()

  active = py.sprite.LayeredUpdates()
  active.layer = {
    "fade": 21,
    "overlay": 20,
    "covers": 19,
    "splash": 10,
    "hints": 9,
    "effects": 8,
    "notes": 7,
    "hitline": 6,
    "lanekeys": 5,
    "lanes": 4,
    "back": 1,
  }
  splash = {each: py.sprite.Group() for each in screen.states}
  splash["select.tracks"] = []


## settings
class ui:
  class font:
    body = "Abel-Regular"
    title = "Rajdhani-Semibold"
    # title = "Orbitron-Semibold"

  class size:
    font = 25
    button = [200, 60]
    
    class select:
      series = [screen.x * 0.6, 120]
      track = [screen.x * 0.3, 120]

  class col:
    back = [0, 23, 42]

    class text:
      idle = [255, 255, 255, 255]
      hover = [255, 255, 255, 255]
      click = [255, 255, 255, 255]
      lock = [255, 255, 255, 128]

    class button:
      idle = [0, 0, 0, 96]
      hover = [144, 64, 241, 128]
      click = [192, 192, 192, 128]
      lock = [0, 0, 0, 64]


class config:
  '''Internal non-alterable settings.'''

  framerate = 60
  faderate = 12

  difficulties = [
    Difficulty("standard", leniency = 0.15, speed = 200),
    Difficulty("advanced", leniency = 0.12, speed = 200),
    Difficulty("expert", leniency = 0.12, speed = 200),
    Difficulty("insane", leniency = 0.12, speed = 200),
  ]

  ranks = [
    Rank("Apex Accurate",
      col = [[], []],
      req = (lambda: level.perfect == len(level.chart.notes) and level.slips == 0),
    ),
    Rank("Apex Perfect",
      col = [[], []],
      req = (lambda: level.perfect == len(level.chart.notes)),
    ),
    Rank("Apex Chain",
      col = [],
      req = (lambda: level.hits == len(level.chart.notes)),
    ),
    Rank("Clear",
      col = 0xffffff,
      req = (lambda: level.score >= config.score.apex * 0.5),
    ),
    Rank("Uhhh...",
      col = 0xffffff,
      req = (lambda: 0 >= level.score),
    ),
    Rank("Finish",
      col = 0x909090,
    ),
  ]

  class score:
    apex: int = 100000
    hit: float = 0.6
    perfect: float = 1

  class keys:
    def _auto_(keys, *, upper = False):
      return {
        key.upper(): vars(py)[
          f"K_{key.upper() if upper else key.lower()}"
        ] for key in keys
      }

    upper = _auto_(["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"])
    home = _auto_(["A", "S", "D", "F", "G", "H", "J", "K", "L"])
    lower = _auto_(["Z", "X", "C", "V", "B", "N", "M"])
    arrows = _auto_(["UP", "LEFT", "DOWN", "RIGHT"], upper = True)
    spec = _auto_(["SPACE", "RETURN", "LSHIFT", "RSHIFT"], upper = True)

    rand = {**upper, **home, **lower}
    all = {**upper, **home, **lower, **arrows, **spec}

  class lane:
    width = 160
    radius = width // 4
    space = 40

  class note:
    size = [120, 10]
    glow = 10

  class effect:
    size = 40
    speed = 8

  sorts = {
    "default": lambda each: each.id,
    "score": lambda each: each,  # TODO
    "name": lambda each: each.track.name,
    "artist": lambda each: each.track.artist,
    "duration": lambda each: each.track.dur,
    # NOTE brackets needed around lambda?
  }


class opt:
  '''User-alterable settings.'''

  framerate = Val(60, lower = 15, upper = 121)
  keys = ["Z", "X", "C", "V"]

  class sound:
    offset = Val(0, lower = -500, upper = 500)
    vol = Val(1.0, lower = 0.0, upper = 1.0)
    music = Val(1.0, lower = 0.0, upper = 1.0)
    effects = Val(1.0, lower = 0.0, upper = 1.0)

  class note:
    highlight = True
    size = Val(1.0, lower = 0.5, upper = 1.0)
    glow = Val(1.0, lower = 0.5, upper = 2.0)

  class effect:
    on = True
    size = Val(1.0, lower = 0.5, upper = 2.0)
    speed = Val(1.0, lower = 0.8, upper = 3.0)

  class col:
    accent = [64, 144, 241, 255]
    flavour = [255, 0, 144, 255]

    hit = [255, 255, 255, 255]
    perfect = [64, 241, 144, 255]
    
    upper = [255, 0, 144, 255]
    home = [64, 241, 144, 255]
    lower = [64, 224, 255, 255]
    spec = [255, 255, 255, 255]
