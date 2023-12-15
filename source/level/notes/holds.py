'''
Implements the `HoldNote` class.
'''

import pygame as pg

from core import level, config, opt

from level.notes import Note


class HoldNote(Note):
  '''A note hit by a pressed and held key.'''

  def __init__(self, hit, **kwargs):
    '''Create a hold note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `num, num` | Beat note should be hit on, and beat it should be held until. |

    Other base parameters are inherited from `Note`.
    '''

    super().__init__(hit, align = (0, -1), **kwargs)

    if hit[0] >= hit[1]:
      raise ValueError("hold note cannot end before it starts")

    self.popping = False  # hold key
    self.popped = False  # key can be let go

    self.slipped = False  # key was let go for too long
    self.poptick = 0  # track how long key has been let go for

  def spawn(self):
    super().spawn()

    self.size = (
      config.note.size[0] * opt.note.size(),
      abs(self.hit[0] - self.hit[1]) * self.speed
    )

    self.surf = ...
    self.surf = pg.Surface(self.size, pg.SRCALPHA)  # FIXME

    pg.draw.rect(self.surf,
      color = (255, 255, 255, 255),
      rect = (0, 0, *self.size),
      width = 0,
      border_radius = round(self.size[0] // 2),
    )

    self.rect = self.surf.get_rect()

  def update(self):
    if not self.popping:
      if level.beat > self.hit[0]:  # note missed
        if self.precision(level.beat, self.hit[0]) == "miss":
          self.slipped = True
    
    else:
      keys = pg.key.get_pressed()
      key = config.keys.all[self.lane.key]
      if not keys[key]:
        self.poptick += 1
        if self.poptick > 2:  # key slipped
          self.slipped = True
      else:
        prec = self.precision(level.beat, self.hit[1])
        if prec and prec != "miss":  # popped within hit timing
          self.popped = True

    super().update()

  def pop(self, hit = False):
    '''Start popping note.'''

    self.popping = True
