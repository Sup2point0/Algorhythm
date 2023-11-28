'''
Implements the game loading sequence.
'''

import math
import random
import json

import pygame as pg

from core import game, screen, config
import util

from splash.text import Text


def load(skip = False):
  '''Run the game loading sequence.'''

  if skip:  # NOTE pending removal
    screen.switch = "start"
    screen.fade = "dark"
    return

  from assets.__toppings__ import flavours

  class load:
    state = None
    tick = 0
    percent = random.randint(7, 20) / 100
    alpha = util.Alpha(0)

    flavour = flavours.select()

  pg.mixer.music.load(f"assets/tracks/dawn{random.randint(1, 3)}.mp3")
  pg.mixer.music.set_volume(0.69)
  pg.mixer.music.play()

  with open("access/data.json", "r+") as file:
    data = json.load(file)

    data["game"]["runs"] += 1
    data["game"]["version"] = game.version

    util.overwrite(file, data)

  ## 2.0 Studios
  while load.tick < 240:
    screen.display.fill((0, 0, 0))
    
    for event in pg.event.get():
      if event.type == pg.QUIT:
        game.state = None
        return
      elif event.type in [pg.KEYDOWN, pg.MOUSEBUTTONDOWN]:
        if 32 < load.tick < 159:
          load.tick = 159
    
    # tick variables
    load.tick += 1
    if 32 < load.tick < 96:
      load.alpha.alt(4)
    elif load.tick > 160:
      load.alpha.alt(-4)

    # render
    rendered = Text.render("2.0 Studios", Text.Style(size = 169, col = pg.Color(255, 0, 144, load.alpha.value)))
    screen.display.blit(rendered[0], util.root(rendered[1]))

    game.pulse.tick(config.rate.frames)
    pg.display.flip()

  ## Loading...
  load.state = True
  load.tick = 0
  while load.state is not None:
    screen.display.fill((0, 0, 2))

    for event in pg.event.get():
      if event.type == pg.QUIT:
        game.state = None
        return
      elif event.type in [pg.KEYDOWN, pg.MOUSEBUTTONDOWN]:
        if load.percent < 1:
          load.percent += random.randint(2, 11) / 600

    # tick variables
    if load.state is True:
      load.tick += 1
      if random.random() < load.percent:
        load.percent += random.randint(2, 13) / 600
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
    screen.display.blit(rendered[0], util.root(rendered[1], y = screen.cy - 50))

    rendered = Text.render(load.flavour, style = Text.Style(
      size = 20,
      col = 3 * [load.alpha.value],
    ))
    screen.display.blit(rendered[0], util.root(rendered[1], y = screen.y - 100))
    
    pg.draw.rect(
      surface = screen.display,
      color = pg.Color(3 * [load.alpha.value]),
      rect = pg.Rect(
        screen.cx - screen.x / 1.6 / 2,
        25 + screen.cy - 25 / 2,
        load.percent * screen.x / 1.6,
        25
      ),
    )

    pg.draw.rect(
      surface = screen.display,
      color = pg.Color(3 * [load.alpha.value]),
      rect = pg.Rect(
        screen.cx - (25 + screen.x / 1.6) / 2,
        25 + screen.cy - 50 / 2,
        25 + screen.x / 1.6,
        50
      ),
      width = 5,
    )

    game.pulse.tick(config.rate.frames)
    pg.display.flip()
  
  screen.switch = "start"
  screen.fade = "dark"