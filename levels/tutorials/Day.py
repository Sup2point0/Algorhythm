'''
Sup#2.0 – Day
'''

from level.level import Chart
from level.action import Action, Hint
from level.notes import (
  TapNote as Tap,
  HoldNote as Hold,
  # RideNote as Ride,
  RollNote as Roll,
)


tutorial = Chart(
  difficulty = 0,
  lanes = 4,
  keys = ["Z", "X", "C", "V"],
  data = [
    Tap(4 * 29, lane = 1),
    Tap(4 * 31, lane = 2),
    Tap(4 * 33, lane = 0), Tap(4 * 33, lane = 3),
    Tap(4 * 35, lane = 1),
    Tap(4 * 36, lane = 2),

    Tap(4 * 39, lane = 0),
    Tap(4 * 39 + 1, lane = 0),
    Tap(4 * 39 + 2, lane = 0),
    Tap(4 * 39 + 3, lane = 0),
    Tap(4 * 40, lane = 1),
    Tap(4 * 40 + 1, lane = 1),
    Tap(4 * 40 + 2, lane = 1),
    Tap(4 * 40 + 3, lane = 1),
    Tap(4 * 41, lane = 2),
    Tap(4 * 41 + 1, lane = 2),
    Tap(4 * 41 + 2, lane = 2),
    Tap(4 * 41 + 3, lane = 2),
    Tap(4 * 42, lane = 3),
    Tap(4 * 42 + 1, lane = 3),
    Tap(4 * 42 + 2, lane = 3),
    Tap(4 * 42 + 3, lane = 3),
  ]
)
