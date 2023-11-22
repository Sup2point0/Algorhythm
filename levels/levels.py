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
      offset = -0.3472,
      vol = 1.0,
      charts = [Day.tutorial],
    ),
    Track("tutorial-advanced",
      name = "ADVANCED TUTORIAL",
      artist = "Sup#2.0",
      file = "Day.wav",
      vol = 1.0,
      charts = [Day.tutorial],
    ),
  ],
  "origins": [],
  "xenos": [],
  "decode": [],
  "special": [],
}
