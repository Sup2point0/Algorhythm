'''
Integrates all the different splash sprite classes into the graphical user interface.
'''

import math
import random
import json

import pygame as py

from core import game, level, screen, sprites, ui, config
from innate import flavour
import util

from splash import roots
from splash.elements import Displayed
from splash.covers import Cover
from splash.asset import Asset
from splash.text import Text, ActiveText
from splash.buttons import Button


def setup():
  '''Load sprites for all screens in the game.'''
  
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

  common = [
    Asset(
      id = "start.backdrop",
      pos = [screen.cx, screen.cy],
      image = "scarlet-cortex.jpg",
      size = screen.size,
      blur = 10,
      display = Displayed(
        hide = {"play", "score"},
        layer = 1,
      ),
    ),
    Button(
      id = "common.back",
      pos = [75, 75],
      size = [ui.button.size[1]] * 2,
      text = "‹",
      root = roots.switch.back,
      display = Displayed(
        hide = {"start", "play", "score"},
        layer = 15,
      ),
    ),
  ]

  pause = [
    ...
  ]

  start = [
    Text(
      id = "start.title",
      pos = util.cord(0, -0.5),
      text = "ALGORHYTHM",
      style = Text.Style(
        typeface = ui.font.title,
        size = 100,
      ),
      display = Displayed(
        show = {"start"},
        layer = 15,
      ),
    ),
    Button(
      id = "start.play",
      pos = util.cord(-0.75, -0.25),
      size = ui.button.size,
      text = "PLAY",
      root = roots.switch.state("home"),
      display = Displayed(
        show = {"start"},
        layer = 15,
      ),
    ),
    Button(
      id = "start.environ",
      pos = util.cord(-0.75, 0),
      size = ui.button.size,
      text = "ENVIRONMENT",
      root = roots.switch.state("environ"),
      display = Displayed(
        show = {"start"},
        layer = 15,
      ),
    ),
    Button(
      id = "start.settings",
      pos = util.cord(-0.75, 0.25),
      size = ui.button.size,
      text = "SETTINGS",
      root = roots.switch.state("settings"),
      display = Displayed(
        show = {"start"},
        layer = 15,
      ),
    ),
    Text(
      id = "start.version",
      pos = [screen.x - 50, screen.y - 50],
      text = "v" + game.version,
      style = Text.Style(
        align = (1, 1),
      ),
      display = Displayed(
        show = {"start"},
        layer = 15,
      ),
    ),
  ]

  environ = []

  settings = [
    Text(
      id = "settings.title",
      pos = util.cord(0, -0.5),
      text = "ALGORHYTHM",
      style = Text.Style(
        typeface = ui.font.title,
        size = 100,
      ),
      display = Displayed(
        show = {"settings"},
        layer = 15,
      ),
    ),
    Text(
      id = "settings.about",
      pos = util.cord(0, -0.25),
      text = f"v{game.version}",
      display = Displayed(
        show = {"settings"},
        layer = 15,
      )
    ),
    Button(
      id = "settings.sounds",
      pos = util.cord(-0.5, 0),
      size = ui.button.size,
      text = "SOUNDS",
      root = roots.switch.state("settings.sounds"),
      display = Displayed(
        show = {"settings"},
        layer = 15,
      ),
    ),
    Button(
      id = "settings.visuals",
      pos = util.cord(0.5, 0),
      size = ui.button.size,
      text = "VISUALS",
      root = roots.switch.state("settings.visuals"),
      display = Displayed(
        show = {"settings"},
        layer = 15,
      ),
    ),
  ]

  account = []

  home = [
    Button(
      id = "home.tutorials",
      pos = util.cord(0, -0.5),
      size = [screen.x * 0.8, ui.button.size[1] * 2],
      text = "TUTORIALS",
      root = roots.switch.state("tutorials"),
      display = Displayed(
        show = {"home"},
        layer = 15,
      ),
    ),
    Button(
      id = "home.origins",
      pos = util.cord(0, -0.25),
      size = [screen.x * 0.8, ui.button.size[1] * 2],
      text = "ORIGINS",
      root = roots.switch.state("origins"),
      display = Displayed(
        show = {"home"},
        layer = 15,
      ),
    ),
    Button(
      id = "home.protos",
      pos = util.cord(0, 0),
      size = [screen.x * 0.8, ui.button.size[1] * 2],
      text = "ORIGINS",
      root = roots.switch.state("protos"),
      display = Displayed(
        show = {"home"},
        layer = 15,
      ),
    ),
    Button(
      id = "home.decode",
      pos = util.cord(0, 0.25),
      size = [screen.x * 0.8, ui.button.size[1] * 2],
      text = "ORIGINS",
      root = roots.switch.state("decode"),
      display = Displayed(
        show = {"home"},
        layer = 15,
      ),
    ),
    Button(
      id = "home.special",
      pos = util.cord(0, 0.5),
      size = [screen.x * 0.8, ui.button.size[1] * 2],
      text = "ORIGINS",
      root = roots.switch.state("special"),
      display = Displayed(
        show = {"home"},
        layer = 15,
      ),
    ),
  ]

  play = [
    ActiveText(
      id = "level.score",
      pos = [screen.x - 40, 40],
      source = lambda: util.setscore(round(level.scored)),
      style = Text.Style(
        size = 69,
        align = (1, -1),
      ),
      display = Displayed(
        show = {"play"},
        layer = 15,
      ),
    ),
    ActiveText(
      id = "level.chain",
      pos = [screen.cx, 40],
      source = lambda: str(level.chain),
      style = Text.Style(
        size = 69,
        align = (0, -1)
      ),
      display = Displayed(
        show = {"play"},
        layer = 15,
      ),
    ),
  ]

  score = []


def loadsequence(display):
  '''Run the game loading sequence.'''

  class load:
    state = None
    tick = 0
    percent = random.randint(7, 20) / 100
    alpha = util.Alpha(0)

    flavour = flavour.flavours.select()

  py.mixer.music.load(f"assets/tracks/dawn{random.randint(1, 3)}.mp3")
  py.mixer.music.set_volume(0.69)
  py.mixer.music.play()

  with open("access/data.json", "r+") as file:
    data = json.load(file)

    data["game"]["runs"] += 1
    data["game"]["version"] = game.version

    util.overwrite(file, data)

  ## 2.0 Studios
  while load.tick < 240:
    display.fill((0, 0, 0))
    
    for event in py.event.get():
      if event.type == py.QUIT:
        game.state = None
        return
      elif event.type in [py.KEYDOWN, py.MOUSEBUTTONDOWN]:
        if 32 < load.tick < 159:
          load.tick = 159
    
    # tick variables
    load.tick += 1
    if 32 < load.tick < 96:
      load.alpha.alt(4)
    elif load.tick > 160:
      load.alpha.alt(-4)

    # render
    rendered = Text.render("2.0 Studios", Text.Style(size = 169, col = py.Color(255, 0, 144, load.alpha.value)))
    display.blit(rendered[0], util.root(rendered[1]))

    game.pulse.tick(config.framerate())
    py.display.flip()

  ## Loading...
  load.state = True
  load.tick = 0
  while load.state is not None:
    display.fill((0, 0, 2))

    for event in py.event.get():
      if event.type == py.QUIT:
        game.state = None
        return
      elif event.type in [py.KEYDOWN, py.MOUSEBUTTONDOWN]:
        if load.percent < 1:
          load.percent += random.randint(2, 11) / 600

    # tick variables
    if load.state is True:
      load.tick += 1
      if random.random() < load.percent:
        load.percent += random.randint(2, 11) / 600
      load.alpha.alt(4)
    else:
      load.state -= 1
      if load.tick - load.state > 96:
        load.state = None
      load.alpha.alt(-4)
      
    if load.percent > 1:
      load.percent = 1
      load.state = load.tick

    # render
    rendered = Text.render("LOADING...", style = Text.Style(
      col = 3 * [load.alpha.value * abs(math.cos(load.tick / 42 - 60))],
    ))
    display.blit(rendered[0], util.root(rendered[1], y = screen.cy - 50))

    rendered = Text.render(load.flavour, style = Text.Style(
      size = 20,
      col = 3 * [load.alpha.value],
    ))
    display.blit(rendered[0], util.root(rendered[1], y = screen.y - 100))
    
    py.draw.rect(
      surface = display,
      color = py.Color(3 * [load.alpha.value]),
      rect = py.Rect(
        screen.cx - screen.x / 1.6 / 2,
        25 + screen.cy - 25 / 2,
        load.percent * screen.x / 1.6,
        25
      ),
    )

    py.draw.rect(
      surface = display,
      color = py.Color(3 * [load.alpha.value]),
      rect = py.Rect(
        screen.cx - (25 + screen.x / 1.6) / 2,
        25 + screen.cy - 50 / 2,
        25 + screen.x / 1.6,
        50
      ),
      width = 5,
    )

    game.pulse.tick(config.framerate())
    py.display.flip()
  
  screen.switch = "start"
  screen.fade = "dark"
