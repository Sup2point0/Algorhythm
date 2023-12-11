'''
Implements the `HoldNote` class.
'''

import pygame as pg

from core import level, config

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

    super().__init__(**kwargs)

    self.hit = hit
    if hit[0] >= hit[1]:
      raise ValueError("hold note cannot end before it starts")

    self.popped = False
    self.slipped = False
    self.popping = False
    self.poptick = 0

  def update(self):
    if not self.popping:
      if level.beat > self.hit[0]:  # note missed
        if self.precision(level.beat, self.hit[0]) == "miss":
          self.slipped = True
    
    else:
      keys = pg.key.get_pressed()
      key = config.keys[self.lane.key]
      if not keys[key]:
        self.poptick += 1
        if self.poptick > 2:  # key slipped
          self.slipped = True
      else:
        acc = self.precision(level.beat, self.hit[1])
        if acc and acc != "miss":  # popped within hit timing
          self.popped = True

  def pop(self, hit = False):
    '''Start popping note.'''

    self.popping = True
