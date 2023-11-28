'''
Day
Sup#2.0
Standard Tutorial
'''

import util

from splash.text import Text

from level.chart import Chart
from level.action import Action, Hint
from level.notes import Tap, Hold, Ride
from level.notes import Taps, Rides


tutorial = Chart(
  difficulty = 0,
  speed = 80,
  keys = ["Z", "X", "C", "V"],
  data = [

    ## intro
    Hint(4 * 1, 6,
      Text("Day.hint.intro.1", util.cord(0, -0.4),
        "Welcome to Algorhythm!"
      ),
    ),
    Hint(4 * 3, 6,
      Text("Day.hint.intro.2", util.cord(0, -0.4),
        "This is a keyboard-based rhythm game."
      ),
    ),
    Hint(4 * 5, 8,
      Text("Day.hint.intro.3", util.cord(0, -0.4),
        "You can pause the game at any time by pressing ESC or clicking the pause button, in the upper left."
      ), [Hint.Highlight(100, 100, 100, 100)]
    ),
    Hint(4 * 8, 8,
      Text("Day.hint.intro.4", util.cord(0, -0.4),
        "Everything should be fairly self-explanatory, but let’s run through how the game works!"
      )
    ),

    ## context
    Hint(4 * 11, 8,
      Text("Day.hint.ctx.1", util.cord(0, -0.4),
        "This is the hitline."
      ),
    ),
    Hint(4 * 14, 8,
      Text("Day.hint.ctx.2", util.cord(0, -0.4),
        "These are the lanes, in which notes approach."
      ),
    ),
    Hint(4 * 17, 8,
      Text("Day.hint.ctx.3", util.cord(0, -0.4),
        "Each lane is assigned its own particular key."
      ),
    ),
    Hint(4 * 20, 8,
      Text("Day.hint.ctx.4", util.cord(0, -0.4),
        "For each lane, you’ll press its key to hit notes in that lane."
      ),
    ),
    Hint(4 * 23, 8,
      Text("Day.hint.ctx.5", util.cord(0, -0.4),
        "Let’s take a look at the different kinds of notes."
      ),
    ),
    
    ## tap notes
    Hint(4 * 26, 8,
      Text("Day.hint.tap.1", util.cord(0, -0.4),
        "When a tap note reaches the hitline, press that lane’s key."
      ),
    ),

    Tap(4 * 28, lane = 1),
    Tap(4 * 30, lane = 2),
    Tap(4 * 32, lane = 0), Tap(4 * 32, lane = 3),
    Tap(4 * 34, lane = 1),
    Tap(4 * 35, lane = 2),

    Hint(16 * 10, 8,
      Text("Day.hint.tap.2", util.cord(0, -0.4),
        "Hit it precisely to the beat to score a perfect hit."
      ),
    ),

    *Taps(0, range(4 * 38, 4 * 39)),
    *Taps(1, range(4 * 39, 4 * 40)),
    *Taps(2, range(4 * 40, 4 * 41)),
    *Taps(3, range(4 * 41, 4 * 42)),

    ## hold notes
    Hint(16 * 12, 8,
      Text("Day.hint.hold.1", util.cord(0, -0.4),
        "When a hold note reaches the hitline, press and hold the lane key until the end of the note."
      ),
    ),

    Hint(16 * 0, 0,
      Text("Day.hint.hold.2", util.cord(0, -0.4),
        "Hitting notes builds your chain, and missing notes breaks it."
      ),
    ),
    
    ## ride notes
    Hint(16 * 0, 0,
      Text("Day.hint.ride.1", util.cord(0, -0.4),
        "When a ride note reaches the hitline, ensure the lane key is already pressed."
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.ride.2", util.cord(0, -0.4),
        "Ride notes do not have to be hit individually, so you can keep the key held down."
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.ride.3", util.cord(0, -0.4),
        "However, it may help to let go at times, to free up fingers."
      ),
    ),
    
    ## finish
    Hint(16 * 0, 0,
      Text("Day.hint.final.1", util.cord(0, -0.4),
        "Now let’s mix everything together!"
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.final.2", util.cord(0, -0.4),
        "Your final score is determined by your precision and highest chain."
      ),
    ),
    Hint(16 * 0, 0,
      Text("Day.hint.final.3", util.cord(0, -0.4),
        "That’s it for now. Enjoy Algorhythm!"
      ),
    ),
  ]
)
