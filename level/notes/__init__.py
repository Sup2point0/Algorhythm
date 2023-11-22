'''
Implements the `TapNote`, `HoldNote`, `RideNote`, `RollNote`, `BreakNote` note kinds, as well as the `Taps`, `Rides` utility functions for mass-creating notes.
'''

from level.notes.taps import TapNote
from level.notes.holds import HoldNote
from level.notes.rides import RideNote
from level.notes.rolls import RollNote
# from level.notes.breaks import BreakNote


def _Notes_(kind):
  '''Internal utility function to create note-generating utility functions.'''
  
  def root(lane, hit) -> list[kind]:
    '''Utility function to create several notes in the same lane at once.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `lane` | `int` | Starting lane of notes. |
    | `hit` | `list`, `range` | Hit beats for each note. This determines how many notes are created. |
    '''

    out = []
    for each in hit:
      out.append(kind(hit = each, lane = lane))
    
    return out

  return root


TapNotes = _Notes_(TapNote)
RideNotes = _Notes_(RideNote)
