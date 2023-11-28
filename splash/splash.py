'''
Integrates all the different splash sprite classes into the graphical user interface.
'''

import pygame as pg

from core import game, level, screen, sprites, ui
import util

from splash import roots
from splash.elements import Displayed
from splash.covers import Cover
from splash.asset import Asset
from splash.text import Text, ActiveText
from splash.buttons import Button
from splash.select import Select, SeriesSelect, TrackSelect

from levels import levels


@ util.log(loaded = False)
def load():
  '''Load sprites for all screens in the game.'''

  # safety net to avoid multiple calls
  if load.loaded:
    return
  
  load.loaded = True

  class displays:
    start = Displayed(
      show = {"start"},
      align = (-1, 0),
    )

  covers = [
    Cover(
      alpha = util.Alpha(255),
      root = roots.fade.total,
    ),
    Cover(
      alpha = util.Alpha(0, bounds = (0, 128)),
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
        show = {"start", "settings", "settings.sounds", "settings.visuals"},
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
      display = displays.start,
    ),
    Button("start.play",
      pos = util.cord(-0.8, -0.1),
      text = "PLAY",
      root = roots.switch.state("select"),
      display = displays.start,
    ),
    Button("start.environ",
      pos = util.cord(-0.8, 0.15),
      text = "ENVIRONMENT",
      root = roots.switch.state("environ"),
      display = displays.start,
    ),
    Button("start.settings",
      pos = util.cord(-0.8, 0.4),
      text = "SETTINGS",
      root = roots.switch.state("settings"),
      display = displays.start,
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
    Asset("environ.backdrop",
      pos = screen.origin,
      image = "cortex-blue.png",
      size = screen.size,
      blur = 5,
      display = Displayed(
        show = {"environ"},
        layer = "backdrop",
      ),
    ),
  ]
  settings = [
    Text("settings.title",
      pos = util.cord(0, -0.5),
      text = "ALGORHYTHM",
      style = Text.Style(
        typeface = ui.font.title,
        size = 100,
      ),
      display = Displayed(show = {"settings"}),
    ),
    Text("settings.about",
      pos = util.cord(0, -0.25),
      text = f"v{game.version}",
      display = Displayed(show = {"settings"})
    ),
    Button("settings.sounds",
      pos = util.cord(-0.5, 0.2),
      text = "SOUNDS",
      root = roots.switch.state("settings.sounds"),
      display = Displayed(show = {"settings"}),
    ),
    Button("settings.visuals",
      pos = util.cord(0.5, 0.2),
      text = "VISUALS",
      root = roots.switch.state("settings.visuals"),
      display = Displayed(show = {"settings"}),
    ),
    Button("settings.visuals",
      pos = util.cord(0, 0.5),
      text = "CREDITS",
      root = roots.switch.state("settings.credits"),
      display = Displayed(show = {"settings"}),
    ),
  ]
  account = [
    ...
  ]
  select = [
    Asset("select.backdrop",
      pos = screen.origin,
      image = "covers/back.jpeg",
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
    SeriesSelect("select.xenos",
      series = "xenos",
      cover = "xenos.jpeg",
    ),
    SeriesSelect("select.decode",
      series = "decode",
      cover = "decode.jpeg",
      lock = (lambda: True),
      locktext = "Arriving in a future update!",
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
    TrackSelect("select.tutorials.standard",
      series = "tutorials",
      track = levels.charts["tutorials"][0],
      cover = "tutorial-standard.jpeg",
    ),
    # *[
    #   TrackSelect(f"select.tutorials.{each.name}",
    #     series = "tutorials",
    #     track = levels.charts["tutorials"][i],
    #     cover = f"tutorial-{each.name}.jpeg",
    #   ) for i, each in enumerate(config.difficulties)
    # ],
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
  score = [
    ...
  ]
