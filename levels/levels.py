'''
Implements all the levels defined in individual files in `levels/` into a single list `charts`.
'''

from level.level import Track

from levels import (
  # Day,
  EndOfTime,
)

# NOTE need `OrderedDict`?
charts = {
  "tutorials": [
    Track("Tutorial",
      file = "end-of-time-instr.mp3",
      bpm = 116,
      offset = 0,
      vol = 1.0,
      charts = [
        EndOfTime.tutorial,
      ]
    ),
  ],
  "origins": [],
  "protos": [],
  "decode": [],
  "special": [],
}
