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
    Hint(16 * 1, 8,
      Text("Day.hint.intro.1", util.cord(0, -0.4),
        "Welcome to Algorhythm!"
      ),
    ),
    Hint(16 * 1.75, 8,
      Text("Day.hint.intro.2", util.cord(0, -0.4),
        "This is a keyboard-based rhythm game."
      ),
    ),
    Hint(16 * 2.5, 12,
      Text("Day.hint.intro.3", util.cord(0, -0.4),
        "You can pause the game at any time by pressing ESC or clicking the pause button, in the upper left."
      )
    ),
    Hint(16 * 3.5, 12,
      Text("Day.hint.intro.4", util.cord(0, -0.4),
        "Everything should be fairly self-explanatory, but let’s run through how the game works!"
      ), [Hint.Highlight(*util.cord(0, 0), 100, 100)]
    ),

    ## context
    Hint(16 * 0, 0,
      Text("Day.hint.ctx.", util.cord(0, -0.4),
        "This is the hitline."
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.ctx.", util.cord(0, -0.4),
        "These are the lanes, in which notes approach."
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.ctx.", util.cord(0, -0.4),
        "Each lane is assigned its own particular key."
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.ctx.", util.cord(0, -0.4),
        "For each lane, you’ll press its key to hit notes in that lane."
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.ctx.", util.cord(0, -0.4),
        "Let’s take a look at the different kinds of notes."
      ),
    ),
    
    ## tap notes
    Hint(16 * 0, 0,
      Text("Day.hint.tap.", util.cord(0, -0.4),
        "When a tap note reaches the hitline, press that lane’s key."
      ),
    ),

    Tap(4 * 29, lane = 1),
    Tap(4 * 31, lane = 2),
    Tap(4 * 33, lane = 0), Tap(4 * 33, lane = 3),
    Tap(4 * 35, lane = 1),
    Tap(4 * 36, lane = 2),

    Hint(16 * 0, 0,
      Text("Day.hint.tap.", util.cord(0, -0.4),
        "Hit it precisely to the beat to score a perfect hit."
      ),
    ),

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

    ## hold notes
    Hint(16 * 0, 0,
      Text("Day.hint.hold.", util.cord(0, -0.4),
        "When a hold note reaches the hitline, press and hold the lane key until the end of the note."
      ),
    ),

    Hint(16 * 0, 0,
      Text("Day.hint.hold.", util.cord(0, -0.4),
        "Hitting notes builds your chain, and missing notes breaks it."
      ),
    ),
    
    ## ride notes
    Hint(16 * 0, 0,
      Text("Day.hint.ride.", util.cord(0, -0.4),
        "When a ride note reaches the hitline, ensure the lane key is already pressed."
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.ride.", util.cord(0, -0.4),
        "Ride notes do not have to be hit individually, so you can keep the key held down."
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.ride.", util.cord(0, -0.4),
        "However, it may help to let go at times, to free up fingers."
      ),
    ),
    
    ## finish
    Hint(16 * 0, 0,
      Text("Day.hint.final.", util.cord(0, -0.4),
        "Now let’s mix everything together!"
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.final.", util.cord(0, -0.4),
        "Your final score is determined by your precision and highest chain."
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.final.", util.cord(0, -0.4),
        "That’s it for now. Enjoy Algorhythm!"
      ),
    ),
  ]
)
