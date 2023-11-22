'''
Implements the `RollNote` class.
'''

import pygame as py

from level.notes import Note


class RollNote(Note):
  '''A note hit by multiple key presses.'''

  def __init__(self, hit, hits, **kwargs):
    '''Create a roll note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `num, num` | Beats at which note reaches and passes the hitline, respectively. |
    | `hits` | `int` | Number of hits required to clear note. |

    Other base parameters are inherited from `Note`.
    '''
    
    if hit[0] >= hit[1]:
      raise ValueError("roll note cannot end before it starts")

    self.hit = hit
    self.hits = hits
