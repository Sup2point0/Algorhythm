'''
Global variables and constants for all modules to access
'''

import pygame as py

# This module is imported by almost every file. As such,
# it should avoid importing any others, otherwise... CIRCULAR IMPORTS!
# These resource modules are an exception, since no other files import them.
from resource.difficulty import Difficulty


## globals
class game:
  '''Game-wide variables.'''

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

  version = "0.0.0"


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


class sprites:
  '''Sprite groups.'''

  splash = py.sprite.Group()
  pause = py.sprite.Group()
  fade = py.sprite.Group()

  lines = py.sprite.Group()
  lanes = py.sprite.Group()
  notes = py.sprite.Group()
  
  active = py.sprite.LayeredUpdates()  # rendered sprites
  '''
  | layer | description |
  | :---- | :---------- |
  | 21 | Overlay |
  | 20 | Screen cover |
  | 10~19 | Splash interface |
  | 9 | Animations |
  | 7~8 | ... |
  | 6 | Notes |
  | 5 | Hitline |
  | 4 | Lanes |
  | 1~3 | Background |
  '''


class screen:
  '''Variables relating to the screen.
  
  `screen.state` and `screen.fade` control what displays on screen. Sprites only render if the current `screen.state` is in their configured list of screen states.
  
  When `screen.switch` is set, `screen.state` is updated to that at the start of the next frame (to avoid conflicting screen state processing within the same frame). While fading out, `screen.fade` becomes `'out'`, freezing sprites from updating. Once the screen entirely blacks out, `screen.fade` briefly becomes `'dark'`. In this time window (where the player cannot see anything), sprites update again, changing the rendered screen.
  '''

  switch = None
  state = None
  '''
  | value | description |
  | :---- | :---------- |
  | `None` | Loading screen. |
  | `start` | Start screen. |
  | `settings` | Settings screen. |
  | `login` | Accounts screen. |
  | `home` | Level selection screen. |
  | `play` | Playing a chart. |
  | `score` | Viewing score after end of level. |
  '''
  
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
  size = [x, y]
  cx = x / 2
  cy = y / 2


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
    text = [255, 255, 255]

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
    apex = 100000
    hit = 0.6
    perfect = 1

  lanewidth = 160
  lanespace = 40
  laneradius = lanewidth // 4

  class keys:
    apex = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    upper = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
    home = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
    lower = ["z", "x", "c", "v", "b", "n", "m"]
    all = apex + upper + home + lower


class opt:
  '''User-alterable settings.'''

  keys = ["z", "x", "c", "v"]

  class col:
    upper = [144, 64, 255]
    home = [255, 144, 32]
    lower = [64, 224, 255]
    spec = [255, 255, 255]
