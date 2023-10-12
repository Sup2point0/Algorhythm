'''
Global variables and constants for all modules to access.
'''

from enum import Enum

import pygame as py

# This module is imported by almost every file. As such,
# it should avoid importing any others, otherwise... CIRCULAR IMPORTS!
# These resource modules are exceptions, since they are safe to import.
from resource.difficulty import Difficulty
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

  events = []  # tracks events in frame
  keys = []  # tracks current pressed keys
  pulse = py.time.Clock()  # game timer


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

  lanewidth = 0
  lanespace = 0


class screen:
  '''Variables relating to the screen.
  
  `screen.state` and `screen.fade` control what displays on screen. Sprites only render if the current `screen.state` is in their configured list of screen states.
  
  When `screen.switch` is set, `screen.state` is updated to that at the start of the next frame (to avoid conflicting screen state processing within the same frame). While fading out, `screen.fade` becomes `'out'`, freezing sprites from updating. Once the screen entirely blacks out, `screen.fade` briefly becomes `'dark'`. In this time window (where the player cannot see anything), sprites update again, changing the rendered screen.
  '''

  switch = None
  state = None
  states = {
    "start", "select",
    *{f"select.{each} for each in [
      "tutorials", "origins", "protos", "decode", "special",
    ]},
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

  track = []

  x = 1280
  y = 720
  cx = x / 2
  cy = y / 2
  size = [x, y]
  origin = [cx, cy]

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


## settings
class ui:
  class font:
    body = "Abel-Regular"
    title = "Orbitron-Semibold"
    size = 25

  class button:
    size = [200, 60]

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
      # idle = [20, 80, 144, 255]
      # hover = [255, 255, 255, 255]
      # click = [255, 255, 255, 144]
      # lock = [128, 128, 128, 255]


class config:
  '''Internal non-user-alterable settings.'''

  framerate = 60
  faderate = 8

  difficulties = [
    Difficulty("standard", leniency = 0.15, speed = 200),
    Difficulty("advanced", leniency = 0.12, speed = 200),
    Difficulty("expert", leniency = 0.12, speed = 200),
    Difficulty("insane", leniency = 0.12, speed = 200),
  ]

  class score:
    apex: int = 100000
    hit: float = 0.6
    perfect: float = 1

  lanewidth = 160
  lanespace = 40
  laneradius = lanewidth // 4

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


class opt:
  '''User-alterable settings.'''

  keys = ["Z", "X", "C", "V"]

  class note:
    size: float = 1.0
    glow: float = 1.0

  class sound:
    offset: float = 0.0
    vol: float = 1.0
    music: float = 1.0
    effects: float = 1.0

  class effect:
    size: float = 1.0
    speed = (15, 8)  ## NOTE simplify?

  class col:
    hit = [255, 255, 255, 255]
    perfect = [64, 241, 144, 255]
    
    upper = [255, 0, 144, 255]
    home = [64, 241, 144, 255]
    lower = [64, 224, 255, 255]
    spec = [255, 255, 255, 255]
