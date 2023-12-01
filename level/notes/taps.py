'''
Implements the `TapNote` note kind.
'''

import pygame as pg

from core import level, config, opt

from level.notes import Note

from effects import blur
from effects.pop import PopEffect


class TapNote(Note):
  '''A note hit by a pressed key.'''

  def __init__(self, *args, **kwargs):
    '''Create a tap note.
    
    All base parameters are inherited from `notes.Note`.
    '''

    super().__init__(*args, **kwargs)

    self.size = (
      config.note.size[0] * opt.note.size(),
      config.note.size[1]
    )

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
    super().update()

  def pop(self, hit = False) -> str | None:
    '''Delete the note and return accuracy.
    
    `hit` determines if it was hit by the player.
    '''
    
    acc = self.accuracy(level.beat, self.hit) if hit else "miss"

    if acc:
      super().pop(acc)
      if acc != "miss":
        PopEffect(pos = self.pos, acc = acc)

    return acc
