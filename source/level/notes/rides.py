'''
Implements the `RideNote` class.
'''

import pygame as pg

from core import level, config, opt

from level.notes import Note

from effects import blur
from effects.pop import PopEffect


class RideNote(Note):
  '''A note hit by a pressed or held key.'''

  def __init__(self, *args, **kwargs):
    '''Create a ride note.

    All base parameters are inherited from `notes.Note`.
    '''

    super().__init__(*args, **kwargs)

    self.size = [
      config.note.size[0] * opt.note.size() * 0.75,
      config.note.size[1]
    ]

  def spawn(self):
    '''Spawn a tap note.'''

    super().spawn()

    self.surf = blur.glow(
      size = self.size,
      dist = 60,
      col = self.col,
      blur = 16,
    )

    pg.draw.rect(self.surf,
      color = (255, 255, 255, 255),
      rect = (60, 60, *self.size),
      width = 0,
      border_radius = round(min(self.size) // 2),
    )
    
    self.rect = self.surf.get_rect()

  def update(self):
    super().move()
    super().out()
    super().update()
    
    # When the note reaches within range of the hitline, check for pops
    keys = pg.key.get_pressed()
    key = config.keys.all[self.lane.key]
    if keys[key]:
      prec = self.precision(level.beat, self.hit)
      if prec and prec != "miss":
        super().pop("perfect")
        PopEffect(pos = self.pos, prec = "perfect")

  def pop(self, hit = False) -> str | None:
    '''Delete the note and return precision.
    
    `hit` determines if it was hit by the player.
    '''
    
    prec = self.precision(level.beat, self.hit) if hit else "miss"

    if prec:
      super().pop(prec)
      if prec != "miss":
        PopEffect(pos = self.pos, prec = prec)

    return prec
