'''
Implements the `Lane` class.
'''

import random

import pygame as pg
from pygame.locals import *

from core import game, level, screen, sprites, config, opt
from innate.sprite import Sprite
import util

from level.notes import Hold
from level.lanekey import LaneKey


class Lane(Sprite):
  '''A lane where notes fall.'''

  def __init__(self, index = None, key = None):
    '''Create a lane.'''

    super().__init__(pos = [screen.cx, 0], align = (0, -1))

    self.index = index
    self.key = key or util.randkey()
    self.col = util.find.col(self.key)
    self.size = [config.lane.width, screen.y - config.lane.space / 2]
    
    self.notes = pg.sprite.Group()
    self.lanekey = LaneKey(self)

    class anim:
      size = [0, 0]
      coltick = 0

    self.anim = anim

  def update(self):
    super().show("lanes")

    ## handle notes
    for event in game.events:
      if event.type == KEYDOWN:
        if event.key == config.keys.all[self.key]:
          self.pop()

    ## animate
    self.anim.size[0] = util.slide(self.anim.size[0], self.size[0], 5)
    self.anim.size[1] = util.slide(self.anim.size[1], self.size[1], 5)

    self.col = util.find.col(self.key)[:3]
    if self.anim.coltick > 0:
      self.anim.coltick -= 0.1
    self.col.append(round(util.interp.val(
      start = 64,
      stop = 255,
      percent = self.anim.coltick
    )))

    ## render
    self.surf = pg.Surface(self.size, pg.SRCALPHA)
    radius = round(config.lane.radius * (self.anim.size[0] / self.size[0]))
    pg.draw.rect(self.surf,
      color = self.col,
      rect = pg.Rect(0, 0, *self.anim.size),
      width = 0,
      border_bottom_left_radius = radius,
      border_bottom_right_radius = radius,
    )
    self.rect = self.surf.get_rect()

    # slide (smoothly) towards correct position
    offset = -(len(sprites.lanes) - 1) / 2 + self.index
    tx = screen.cx + offset * (config.lane.width + config.lane.space)
    self.x = util.slide(self.x, tx, 5)

    super().position()

    self.lanekey.update()

  def pop(self):
    '''Attempt to hit the closest note in the lane.'''

    notes = self.notes.sprites()

    if notes:
      notes = sorted(notes, key = lambda note: (note.hit, -note.y))
      for note in notes:
        if isinstance(note, Hold):
          if not note.popping:
            note.pop(hit = True)
            break
        else:
          note.pop(hit = True)
          break
    
    else:
      level.slips += 1

    self.anim.coltick = 0.4

  def switch(self, index = None):
    '''Change index of lane.'''

    lanes = sorted(sprites.lanes.sprites(), key = lambda lane: lane.index)
    lanes.pop(self.index)
    if index is None:
      index = random.choice([i for i in range(len(lanes)) if i != self.index])
    lanes.insert(index, self)
    
    for lane in lanes:
      lane.index = lanes.index(lane)
