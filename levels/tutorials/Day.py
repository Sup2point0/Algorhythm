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


## NOTE testing
from random import randint
data = []
t = 4
# for k in range(12):
#   for i in range(20):
#     t += randint(1, 4) / 4
#     data.append(TapNote(hit = t, speed = (k + 1) * 50))

for i in range(128):
  t += randint(1, 2) / 2
  # t += 1
  for i in range(1, randint(1, 3)):
    data.append(Tap(hit = t + 4, speed = 300))

# for i in range(16):
#   data.append(TapNote(hit = i + 4, lane = 0))
###


tutorial = Chart(
  difficulty = 0,
  lanes = 4,
  keys = ["Z", "X", "C", "V"],
  data = [
    # TODO Make the tutorial level!
    *data
  ]
)
