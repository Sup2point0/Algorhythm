'''
Implements the `TapNote` note kind.
'''

import pygame as py

from core import level, config, opt

from level.notes import Note

from effects import blur
from effects.pop import PopEffect


class TapNote(Note):
  '''A note hit by a pressed key.'''

  def __init__(self, hit, **kwargs):
    '''Create a tap note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `num` | Beat note should be hit on. |

    Other base parameters are inherited from `Note`.
    '''

    super().__init__(**kwargs)

    self.hit = hit

    self.size = (
      config.note.size[0] * opt.note.size(),
      config.note.size[1]
    )

  def spawn(self):
    '''Spawn a tap note.'''

    super().spawn()

    self.surf = blur.glow(
      size = self.size,
      dist = 50,
      col = self.col,
      blur = 40,
    )

    py.draw.rect(self.surf,
      color = (255, 255, 255, 255),
      rect = (50, 50, *self.size),
      width = 0,
      border_radius = round(min(self.size) // 2),
    )
    
    self.rect = self.surf.get_rect()

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
