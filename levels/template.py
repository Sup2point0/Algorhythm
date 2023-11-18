'''
Artist – Track
'''

from level.level import Chart
from level.action import Action
from level.notes import (
  TapNote as Tap,
  HoldNote as Hold,
  RideNote as Ride,
  RollNote as Roll,
  # BreakNote as Break,
  TapNotes as Taps,
  RideNotes as Rides,
)


standard = Chart(
  difficulty = 0,
  lanes = 4,
  data = [
    ...
  ]
)
