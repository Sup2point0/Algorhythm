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


'''
This is the hitline.
These are the lanes, in which notes approach.
Each lane is assigned its own particular key.
For each lane, you’ll press its key to hit notes in that lane.
Let’s take a look at the different kinds of notes.
——
When a tap note reaches the hitline, press that lane’s key.
Hit it precisely to the beat to score a perfect hit.
When a hold note reaches the hitline, press and hold the lane key until the end of the note.
Hitting notes builds your chain, and missing notes breaks it.
——
When a ride note reaches the hitline, ensure the lane key is already pressed.
Ride notes do not have to be hit individually, so you can keep the key held down.
However, it may help to let go at times, to free up fingers.
——
Now let’s mix everything together!
Your final score is determined by your precision and highest chain.
That’s it for now. Enjoy Algorhythm!
'''


tutorial = Chart(
  difficulty = 0,
  lanes = 4,
  keys = ["Z", "X", "C", "V"],
  data = [
    Hint(4, 8,
      Text("Day.hint.1", util.cord(0, 0.8), "Welcome to Algorhythm!"),
      [Hint.Highlight(*util.cord(0, 0), 100, 100)]
    ),
    Hint(16, 8,
      Text("Day.hint.2", util.cord(0, 0.8), "This is a keyboard-based rhythm game."),
      [Hint.Highlight(*util.cord(0, 0), 100, 100)]
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
