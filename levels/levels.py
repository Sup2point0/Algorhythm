'''
Implements all the levels defined in individual files in `levels/` into a single list `charts`.
'''

from level.level import Track

from levels import (
  Day,
  EndOfTime,
)


charts = [
  Track("Tutorial",
    file = "end-of-time-instr.mp3",
    bpm = 116,
    offset = 0,
    vol = 1.0,
    charts = [
      EndOfTime.tutorial,
    ]
  ),
  # Track("Playmaker – Victory Theme",
  #   artist = "Duel Links – VRAINS World",
  #   file = "playmaker.mp3",
  #   bpm = 149.9957,
  #   offset = 99.5,
  #   vol = 1.0,
  #   charts = [
  #     Playmaker.standard,
  #   ]
  # ),
]
