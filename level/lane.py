'''
Note lanes
'''

import random

import pygame as py
from pygame.locals import *

from core import game, level, screen, sprites, ui, config, opt
import util

from level.lanekey import LaneKey


class Lane(py.sprite.Sprite):
  '''A lane where notes fall.'''

  def __init__(self, index = None, key = None):
    '''Create a lane.'''

    super().__init__()

    self.index = index
    self.key = key or util.randkey()
    self.hit = False
    self.col = util.find.col(self.key)

    self.x = screen.cx - 1
    self.y = 0
    self.cx = screen.cx
    self.size = [config.lanewidth, screen.y - config.lanespace / 2]
    self.notes = py.sprite.Group()

    self.lanekey = LaneKey(self)

    class anim:
      size = [2, 2]
      coltick = 0

    self.anim = anim

  def update(self):
    sprites.active.add(self, layer = sprites.active.layer["lanes"])

    ## handle notes
    for event in game.events:
      if event.type in [KEYDOWN, KEYUP]:
        if event.key == globals()[f"K_{self.key}"]:
          self.hit = (event.type == KEYDOWN)

    if self.hit:
      self.pop()

    ## animate
    self.anim.size[0] = util.slide(self.anim.size[0], self.size[0], 5)
    self.anim.size[1] = util.slide(self.anim.size[1], self.size[1], 5)

    self.col = vars(opt.col)[util.find.row(self.key)][:3]
    if self.anim.coltick > 0:
      self.anim.coltick -= 0.1
    self.col.append(round(util.interpolate.value(
      start = 64,
      stop = 255,
      percent = self.anim.coltick
    )))

    ## render
    self.image = py.Surface(self.size, py.SRCALPHA)
    radius = round(config.laneradius * (self.anim.size[0] / self.size[0]))
    py.draw.rect(
      surface = self.image,
      color = py.Color(self.col),
      rect = py.Rect(0, 0, *self.anim.size),
      width = 0,
      border_bottom_left_radius = radius,
      border_bottom_right_radius = radius,
    )
    self.rect = self.image.get_rect()

    # slide (smoothly) towards correct position
    offset = -(len(sprites.lanes) - 1) / 2 + self.index
    self.cx = screen.cx + offset * (config.lanewidth + config.lanespace)
    tx = util.root(self.rect, x = self.cx)[0]
    self.x = round(util.slide(self.x, tx, 5))

    self.rect.topleft = [self.x, self.y]

  def pop(self):
    '''Attempt to hit the closest note in the lane.'''

    notes = self.notes.sprites()
    if notes:
      note = sorted(notes, key = lambda note: note.hit)[0]
      note.pop(hit = True)

    self.anim.coltick = 0.4

    self.hit = False

  def switch(self, index = None):
    '''Change index of lane.'''

    lanes = sorted(sprites.lanes.sprites(), key = lambda lane: lane.index)
    lanes.pop(self.index)
    if index is None:
      index = random.choice([i for i in range(len(lanes)) if i != self.index])
    lanes.insert(index, self)
    
    for lane in lanes:
      lane.index = lanes.index(lane)
