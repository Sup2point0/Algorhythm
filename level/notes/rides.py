'''
Implements the `RideNote` class.
'''

import pygame as py

from core import config, opt

from level.notes import Note


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
