'''
Day
Sup#2.0
Standard Tutorial
'''

import util

from splash.text import Text

from level.level import Chart
from level.action import Action, Hint
from level.notes import Tap, Hold, Ride
from level.notes import Taps, Rides


tutorial = Chart(
  difficulty = 0,
  lanes = 4,
  keys = ["Z", "X", "C", "V"],
  data = [
    Hint(16 * 1, 12,
      Text("Day.hint.1", util.cord(0, 0.8),
        "Welcome to Algorhythm!"
      ),
    ),
    Hint(16 * 2, 12,
      Text("Day.hint.2", util.cord(0, 0.8),
        "This is a keyboard-based rhythm game."
      ),
    ),
    Hint(16 * 3, 12,
      Text("Day.hint.2", util.cord(0, 0.8),
        "You can pause the game at any time by pressing ESC or clicking the pause button, in the upper left."
      )
    ),
    Hint(16 * 4, 12,
      Text("Day.hint.2", util.cord(0, 0.8),
        "Everything should be fairly self-explanatory, but let’s run through how the game works!"
      ), [Hint.Highlight(*util.cord(0, 0), 100, 100)]
    ),

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
