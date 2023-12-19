'''
Integrates all the different splash sprite classes into the graphical user interface.
'''

import pygame as pg

from core import game, level, screen, sprites, ui, config
from innate import Alpha
import util

from splash import roots, presets
from splash.elements import Displayed
from splash.covers import Cover
from splash.asset import Asset
from splash.text import Text, Textbox, ActiveText
from splash.buttons import Button
from splash.select import Select, SeriesSelect, TrackSelect
from splash.views.results import LevelResults

from levels import levels


@ util.log(loaded = False)
def load():
  '''Load sprites for all screens in the game.'''

  # safety net to avoid multiple calls
  if load.loaded:
    return
  
  load.loaded = True

  covers = [
    Cover(
      alpha = Alpha(255),
      root = roots.fade.total,
    ),
    Cover(
      alpha = Alpha(0, bounds = (0, 128)),
      root = roots.fade.partial,
    ),
  ]
  general = [
    Button("general.back",
      pos = [50, 50],
      text = "‹",
      root = roots.switch.back,
      style = Button.Style(
        size = (ui.size.button[1], ui.size.button[1]),
      ),
      display = Displayed(
        hide = {"start", "play", "score"},
        align = (-1, -1),
      ),
    ),
  ]
  pause = [
    ...
  ]
  start = [
    Asset("start.backdrop",
      pos = screen.origin,
      image = "cortex-violet.jpg",
      size = screen.size,
      blur = 5,
      display = Displayed(
        show = {"start", "set",
          "set.sounds", "set.visuals",
          "set.changelog", "set.credits"},
        layer = "backdrop",
      ),
    ),
    Text("start.title",
      pos = util.cord(-0.8, -0.6),
      text = "ALGORHYTHM",
      style = Text.Style(
        typeface = ui.font.title,
        size = 100,
      ),
      display = presets.display.start,
    ),
    Button("start.play",
      pos = util.cord(-0.8, -0.1),
      text = "PLAY",
      root = roots.switch.state("select"),
      display = presets.display.start,
    ),
    Button("start.environ",
      pos = util.cord(-0.8, 0.15),
      text = "ENVIRONMENT",
      root = roots.switch.state("env"),
      display = presets.display.start,
    ),
    Button("start.settings",
      pos = util.cord(-0.8, 0.4),
      text = "SETTINGS",
      root = roots.switch.state("set"),
      display = presets.display.start,
    ),
    Text("start.version",
      pos = [screen.x - 50, screen.y - 50],
      text = "v" + game.version,
      style = Text.Style(
        align = (1, 1),
      ),
      display = Displayed(
        show = {"start"},
        align = (1, 1),
      ),
    ),
  ]

  environ = [
    Asset("env.backdrop",
      pos = screen.origin,
      image = "cortex-blue.png",
      size = screen.size,
      blur = 5,
      display = Displayed(
        show = {"env"},
        layer = "backdrop",
      ),
    ),
    LevelResults("",
      pos = (screen.cx, screen.cy * 0.5),
      display = Displayed(
        show = {"env"},
        align = (-1, -1),
      ),
    )
  ]

  settings = [
    Text("set.title",
      pos = util.cord(0, -0.6),
      text = "ALGORHYTHM",
      style = Text.Style(
        typeface = ui.font.title,
        size = 100,
      ),
      display = Displayed(show = {"set"}),
    ),
    Text("set.version",
      pos = util.cord(0, -0.35),
      text = f"v{game.version}",
      display = Displayed(show = {"set"})
    ),
    Button("set.sounds",
      pos = util.cord(-0.25, 0.15),
      text = "SOUNDS",
      root = roots.switch.state("set.sounds"),
      display = Displayed(show = {"set"}),
    ),
    Button("set.visuals",
      pos = util.cord(0.25, 0.15),
      text = "VISUALS",
      root = roots.switch.state("set.visuals"),
      display = Displayed(show = {"set"}),
    ),
    Button("set.changelog",
      pos = util.cord(-0.25, 0.4),
      text = "CHANGELOG",
      root = roots.switch.state("set.changelog"),
      display = Displayed(show = {"set"}),
    ),
    Button("set.credits",
      pos = util.cord(0.25, 0.4),
      text = "CREDITS",
      root = roots.switch.state("set.credits"),
      display = Displayed(show = {"set"}),
    ),
  ]
  sounds = []
  visuals = []
  changelog = []
  credits = [
    Text("set.credits.title",
      pos = util.cord(0, -0.6),
      text = "ALGORHYTHM",
      style = Text.Style(
        typeface = ui.font.title,
        size = 100,
      ),
      display = presets.display.credits,
    ),
    Text("set.credits.version",
      pos = util.cord(0, -0.35),
      text = f"v{game.version}",
      display = presets.display.credits,
    ),
    Text("set.credits.creator",
      pos = util.cord(0, -0.1),
      text = f"by Sup#2.0",
      display = presets.display.credits,
    ),
    Textbox("set.credits.1",
      pos = util.cord(0, 0.2),
      text = [
        "made in Python 3.11",
        "with Pygame 2.5",
      ],
      display = presets.display.credits,
    ),
    Text("set.credits.playtesters",
      pos = util.cord(0, 0.5),
      text = f"Playtesters",
      style = Text.Style(
        typeface = ui.font.title,
        size = 40,
      ),
      display = presets.display.credits,
    ),
    Textbox("set.credits.2",
      pos = util.cord(0, 1.0),
      text = [
        "Sup#1.2",
        "iTechnical",
      ],
      display = presets.display.credits,
    ),
    Text("set.credits.packages",
      pos = util.cord(0, 0.5),
      text = f"Packages",
      style = Text.Style(
        typeface = ui.font.title,
        size = 40,
      ),
      display = presets.display.credits,
    ),
    Textbox("set.credits.3",
      pos = util.cord(0, 1.0),
      text = [
        "Pillow",
        "image effects",
        " ",
        "Librosa",
        "sound processing",
        "",
        "test",
      ],
      display = presets.display.credits,
    ),
    Text("set.credits.fonts",
      pos = util.cord(0, 0.5),
      text = f"Fonts",
      style = Text.Style(
        typeface = ui.font.title,
        size = 40,
      ),
      display = presets.display.credits,
    ),
    Textbox("set.credits.3",
      pos = util.cord(0, 1.0),
      text = [
        "Pillow",
        "image effects",
        " ",
        "Librosa",
        "sound processing",
        "",
        "test",
      ],
      display = presets.display.credits,
    ),
  ]

  account = [
    ...
  ]

  select = [
    Asset("select.backdrop",
      pos = screen.origin,
      image = "covers/select.jpeg",
      size = screen.size,
      blur = 5,
      display = Displayed(
        show = {"select"},
        layer = "backdrop",
      ),
    ),
    SeriesSelect("select.tutorials",
      series = "tutorials",
      cover = "tutorials.jpeg",
    ),
    SeriesSelect("select.origins",
      series = "origins",
      cover = "origins.jpeg",
    ),
    SeriesSelect("select.roots",
      series = "roots",
      cover = "roots.jpeg",
    ),
    SeriesSelect("select.decode",
      series = "decode",
      cover = "decode.jpeg",
      lock = (lambda: True),
      locktext = "Arriving in a future update!",
    ),
    SeriesSelect("select.encode",
      series = "encode",
      cover = "encode.jpeg",
      lock = (lambda: True),
      locktext = "Arriving in a future update!",
    ),
    SeriesSelect("select.xenos",
      series = "xenos",
      cover = "xenos.jpeg",
    ),
    SeriesSelect("select.special",
      series = "special",
      cover = "special.jpeg",
    ),
    Button("select.track.play",
      pos = [screen.x - 50, screen.y - 50],
      text = "PLAY",
      root = roots.switch.tutorial,
      display = Displayed(
        show = {state for state in screen.states if state.startswith("select.")},
        align = (1, 1),
      ),
    ),
  ]
  tutorials = [
    Asset("select.tutorials.backdrop",
      pos = screen.origin,
      image = "covers/tutorial-standard.jpeg",
      size = screen.size,
      blur = 5,
      dark = 32,
      display = Displayed(
        show = {"select.tutorials"},
        layer = sprites.active.layer["backdrop"],
      ),
    ),
    # TrackSelect("select.tutorials.standard",
    #   series = "tutorials",
    #   track = levels.charts["tutorials"][0],
    #   cover = "tutorial-standard.jpeg",
    # ),
    *[
      TrackSelect(f"select.tutorials.{each.name}",
        series = "tutorials",
        track = levels.charts["tutorials"][i],
        cover = f"tutorial-{each.name}.jpeg",
      ) for i, each in enumerate(config.difficulties[:2])
    ],
  ]

  play = [
    ActiveText("level.score",
      pos = [screen.x - 40, 40],
      source = lambda: util.setscore(round(level.scored)),
      style = Text.Style(
        size = 69,
      ),
      display = Displayed(
        show = {"play"},
        align = (1, -1)
      ),
    ),
    ActiveText("level.chain",
      pos = [screen.cx, 40],
      source = lambda: str(level.chain),
      style = Text.Style(
        size = 69,
      ),
      display = Displayed(
        show = {"play"},
        align = (0, -1)
      ),
    ),
  ]

  results = [
    ...
  ]
