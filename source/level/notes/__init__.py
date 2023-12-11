'''
Implements the `Tap`, `Hold`, `Ride`, `Roll`, `Break` note kinds, as well as the `Taps`, `Rides` utility functions for mass-creating notes.
'''

from level.notes.note import Note
from level.notes.taps import TapNote as Tap
from level.notes.holds import HoldNote as Hold
from level.notes.rides import RideNote as Ride
from level.notes.rolls import RollNote as Roll
# from level.notes.breaks import BreakNote as Break


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


Taps = _Notes_(Tap)
Rides = _Notes_(Ride)
