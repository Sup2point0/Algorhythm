'''
Graphic interface functionality
'''

import math
import random as ran

import pygame as py

from core import game, level, screen, ui, config
import util
from resource import flavour

from splash import roots
from splash.covers import Cover
from splash.asset import Asset
from splash.text import Text, ActiveText
from splash.buttons import Button


def setup():
  '''Load sprites for all screens in the game.'''
  
  covers = [
    Cover(alpha = 255, root = roots.fade.total),
    Cover(alpha = 0, root = roots.fade.partial, bounds = (0, 128)),
  ]

  common = [
    Button(
      id = "common.back",
      pos = [100, 55],
      size = [150, ui.button.size[1]],
      text = "BACK",
      root = roots.switch.back,
      display = {"start": False, "play": False, "score": False},
    ),
  ]

  pause = [
    
  ]

  start = [
    ## NOTE: code for image asset
    # Asset(
    #   id = "start.title",
    #   pos = [screen.cx, screen.cy * 0.5],
    #   image = "Algorhythm.png",
    #   display = ["start"],
    # ),
    Text(
      id = "start.title",
      pos = [screen.cx, screen.cy * 0.5],
      text = "ALGORHYTHM",
      display = ["start"],
      style = Text.Style(
        typeface = "Orbitron-Semibold",
        size = 100,
      ),
    ),
    Button(
      id = "start.play",
      pos = [screen.cx, screen.cy * 1.0],
      size = ui.button.size,
      text = "PLAY",
      root = roots.switch.state("home"),
      display = ["start"],
    ),
    Button(
      id = "start.tutorial",
      pos = [screen.cx, screen.cy * 1.25],
      size = ui.button.size,
      text = "TUTORIAL",
      root = roots.switch.tutorial,
      display = ["start"],
    ),
    Button(
      id = "start.settings",
      pos = [screen.cx, screen.cy * 1.5],
      size = ui.button.size,
      text = "SETTINGS",
      root = roots.switch.state("settings"),
      display = ["start"],
    ),
    Text(
      id = "start.version",
      pos = [screen.x - 50, screen.y - 50],
      text = "v" + game.version,
      display = ["start"],
      style = Text.Style(
        align = (1, 1),
      )
    ),
  ]

  settings = [
    Text(
      id = "settings.title",
      pos = [screen.cx, screen.cy * 0.5],
      text = "SETTINGS",
      display = ["settings"],
      style = Text.Style(
        typeface = "Orbitron-Semibold",
        size = 100,
      ),
    ),
  ]

  home = [

  ]

  play = [
    ActiveText(
      id = "level.score",
      pos = [screen.x - 40, 40],
      source = lambda: util.setscore(round(level.scored)),
      display = ["play"],
      style = Text.Style(
        size = 69,
        align = (1, -1),
      )
    ),
    ActiveText(
      id = "level.chain",
      pos = [screen.cx, 40],
      source = lambda: str(level.chain),
      display = ["play"],
      style = Text.Style(
        size = 69,
        align = (0, -1)
      )
    ),
  ]


def loadsequence(display):
  '''Run the game loading sequence.'''

  class load:
    state = None
    tick = 0
    percent = ran.randint(7, 20) / 100
    alpha = util.Alpha(0)

    flavour = flavour.flavours.select()

    py.mixer.music.load(f"assets/tracks/dawn{ran.randint(1, 3)}.m4a")
    py.mixer.music.set_volume(0.69)
    py.mixer.music.play()

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

    game.pulse.tick(config.framerate)
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
          load.percent += ran.randint(2, 9) / 600

    # tick variables
    if load.state is True:
      load.tick += 1
      if ran.random() < load.percent:
        load.percent += ran.randint(2, 9) / 600
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

    game.pulse.tick(config.framerate)
    py.display.flip()

  screen.switch = "start"
  screen.fade = "dark"
