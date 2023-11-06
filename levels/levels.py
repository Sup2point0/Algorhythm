'''
Implements all the levels defined in individual files in `levels/` into a single list `charts`.
'''

from level.level import Track

from levels.tutorials import Day


charts = {
  "tutorials": [
    Track("tutorial-standard",
      name = "STANDARD TUTORIAL",
      artist = "Sup#2.0",
      file = "Day.wav",
      bpm = 144,
      offset = 0,
      vol = 1.0,
      charts = [Day.tutorial]
    ),
    Track("tutorial-advanced",
      name = "ADVANCED TUTORIAL",
      artist = "Sup#2.0",
      file = "end-of-time-instr.mp3",
      bpm = 116,
      offset = 0,
      vol = 1.0,
      charts = [] #[Daylight.tutorial],
    )
  ],
  "origins": [],
  "xenos": [],
  "decode": [],
  "special": [],
}
