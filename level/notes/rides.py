'''
Implements the `RideNote` class.
'''

import pygame as py

from core import config

from level.notes import Note


class RideNote(Note):
  '''A note hit by a pressed or held key.'''

  def __init__(self, hit, **kwargs):
    '''Create a ride note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `num` | Beat note should be hit on. |

    Other base parameters are inherited from `notes.Note`.
    '''

    super().__init__(**kwargs)

    self.hit = hit

    self.size = [
      config.note.size[0] * opt.note.size() * 0.75,
      config.note.size[1]
    ]