'''
Day
Sup#2.0
Standard Tutorial
'''

from core import screen, config
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
    Hint(4*1, 8,
      Text("Day.hint.intro.1", util.cord(0, -0.4),
        "Welcome to Algorhythm!"
      ),
    ),
    Hint(4*4, 8,
      Text("Day.hint.intro.2", util.cord(0, -0.4),
        "This is a keyboard-based rhythm game."
      ),
    ),
    Hint(4*7, 8,
      Text("Day.hint.intro.3", util.cord(0, -0.4),
        "You can pause the game at any time by pressing ESC or clicking the pause button, in the upper left."
      ), [Hint.Highlight(100, 100, 150, 150)]
    ),
    Hint(4*10, 8,
      Text("Day.hint.intro.4", util.cord(0, -0.4),
        "Everything should be fairly self-explanatory, but let’s run through how the game works!"
      )
    ),

    ## context
    Hint(4*13, 6,
      Text("Day.hint.ctx.1", util.cord(0, -0.4),
        "This is the hitline."
      ), [Hint.Highlight(screen.cx, screen.y - config.lane.space * 4, screen.x, 50)]
    ),
    Hint(4*16, 8,
      Text("Day.hint.ctx.2", util.cord(0, -0.4),
        "These are the lanes."
      ), [Hint.Highlight(*screen.origin, config.lane.width * 4 + config.lane.space * 5, screen.y)]
    ),
    Hint(4*19, 8,
      Text("Day.hint.ctx.3", util.cord(0, -0.4),
        "Each lane has its own key."
      ), [Hint.Highlight(screen.cx, screen.y - config.lane.space * 2, config.lane.width * 4 + config.lane.space * 6, 100)]
    ),
    Hint(4*22, 8,
      Text("Day.hint.ctx.5", util.cord(0, -0.4),
        "Let’s take a look at the different kinds of notes."
      ),
    ),
    
    ## tap notes
    Hint(4*26, 8,
      Text("Day.hint.tap.1", util.cord(0, -0.4),
        "When a tap note reaches the hitline, press that lane’s key."
      ), [Hint.Highlight(
        screen.cx - (config.lane.space + config.lane.width) / 2, screen.cy,
        config.lane.width + config.lane.space * 2, screen.y
      )]
    ),

    Tap(4*28, lane = 1),
    Tap(4*30, lane = 2),
    Tap(4*32, lane = 0), Tap(4*32, lane = 3),
    Tap(4*34, lane = 1),
    Tap(4*35, lane = 2),

    Hint(4*36, 8,
      Text("Day.hint.tap.2", util.cord(0, -0.4),
        "Hit it precisely to the beat to score a perfect hit."
      ),
    ),

    *Taps(0, range(4*38, 4*39)),
    *Taps(1, range(4*39, 4*40)),
    *Taps(2, range(4*40, 4*41)),
    *Taps(3, range(4*41, 4*42)),

    ## hold notes
    Hint(4*42, 8,
      Text("Day.hint.hold.1", util.cord(0, -0.4),
        "When a hold note reaches the hitline, press and hold the lane key until the end of the note."
      ),
    ),

    Hold((4*44, 4*46 -2), lane = 2),
    Hold((4*46, 4*48 -2), lane = 1),
    Hold((4*48, 4*50 -2), lane = 3),
    Hold((4*50, 4*51 -2), lane = 0),
    Hold((4*51, 4*52 -2), lane = 2),

    Hint(4*51, 8,
      Text("Day.hint.hold.2", util.cord(0, -0.4),
        "Hitting notes builds your chain, and missing notes breaks it."
      ),
    ),
    
    ## ride notes
    Hint(4*60, 8,
      Text("Day.hint.ride.1", util.cord(0, -0.4),
        "When a ride note reaches the hitline, ensure the lane key is already pressed."
      ),
    ),
    Hint(4*63, 8,
      Text("Day.hint.ride.2", util.cord(0, -0.4),
        "Ride notes do not have to be hit individually, so you can keep the key held down."
      ),
    ),

    *Rides(0, util.beats(4*64, 4*66, 0.5)),
    *Rides(0, util.beats(4*66, 4*68, 0.5)),

    Hint(4*66, 8,
      Text("Day.hint.ride.3", util.cord(0, -0.4),
        "However, it may help to let go at times, to free up fingers."
      ),
    ),
    
    ## finish
    Hint(4*75, 6,
      Text("Day.hint.final.1", util.cord(0, -0.4),
        "Now let’s mix everything together!"
      ),
    ),
    Hint(4*88, 8,
      Text("Day.hint.final.2", util.cord(0, -0.4),
        "Your final score is determined by your precision and highest chain."
      ),
    ),
    Hint(4*92, 8,
      Text("Day.hint.final.3", util.cord(0, -0.4),
        "That’s it for now. Enjoy Algorhythm!"
      ),
    ),
  ]
)
