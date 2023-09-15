'''
Level handling
'''


from pygame import mixer

from core import game, level, screen, sprites, config, opt
import util

from level.hitline import Hitline
from level.lane import Lane
from level.notes import Note
from level.action import Action


class Chart:
  '''An Algorhythm level.'''

  def __init__(self,
    difficulty: int,
    lanes: int = 4,
    keys: list = opt.keys,
    data = list(),
  ):
    '''Create a chart.
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    ''' # TODO

    self.difficulty = difficulty
    self.data = data
    self.lines = [each for each in data if isinstance(each, Hitline)] or Hitline()
    self.notes = [each for each in data if isinstance(each, Note)]
    self.actions = [each for each in data if isinstance(each, Action)]

    self.lanes = []
    for i in range(lanes):
      self.lanes.append(Lane(index = i, key = keys[i]))


class Track:
  '''A particular soundtrack.'''

  def __init__(self,
    name,
    bpm,
    file: str,
    offset: float,
    vol: float = 1.0,
    artist = None,
    charts: list = None,
  ):
    '''Create a soundtrack.
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    | `name` | `str` | Song name. |
    | `artist` | `str` | Song artist. |
    | `bpm` | `int`, `float` | Beats per minute. |
    | `file` | `str` | Source file to stream from. |
    | `offset` | `float` | Time offset until song should start playing. |
    | `vol` | `float` | Internal volume of song. |
    | `charts` | `list[Chart]` | Playable charts of the song. |
    '''

    self.name = name
    self.artist = artist
    self.bpm = bpm
    self.file = file
    self.offset = offset
    self.vol = vol
    self.charts = sorted(charts, key = lambda chart: chart.difficulty) or []
    self.difficulties = (chart.difficulty for chart in self.charts)

  def __getitem__(self, difficulty):
    ''''''

    for chart in self.charts:
      if chart.difficulty == difficulty:
        return chart
    else:
      return None
      # if chart not found, return no value and handle accordingly

  def start(self, difficulty: int):
    '''Start a new game with a selected difficulty.'''

    game.level = self
    level.chart = self[difficulty]
    level.beat = 0
    level.tick = 0
    level.score = 0
    level.scored = 0
    level.hits = 0
    level.perfect = 0
    level.chain = 0
    level.apex = 0
    level.lanespace = config.lanespace

    # clear just to be safe
    sprites.lines.empty()
    sprites.lanes.empty()
    sprites.notes.empty()

    sprites.lines.add(level.chart.lines)
    sprites.lanes.add(level.chart.lanes)
    for note in level.chart.notes:
      note.spawn()
      sprites.notes.add(note)
    
    mixer.music.fadeout(1000)

    level.started = False  # only becomes True once music starts

  def run(self):
    '''Process and control chart.'''
    
    level.tick += 1

    ## start or end level
    if not mixer.music.get_busy():
      if not level.started:
        if level.tick > 60:
          mixer.music.load(f"assets/tracks/{self.file}")
          mixer.music.set_volume(self.vol)
          mixer.music.play()
          level.started = True
      else:
        return self.end()
    
    ## process level
    if level.started:
      level.beat = game.level.bpm * (mixer.music.get_pos() - game.level.offset) / 60000

    for action in level.chart.data:
      if isinstance(action, Action):
        action.activate()

    ## handle notes
    sprites.lines.update()
    sprites.notes.update()
    sprites.lanes.update()
    sprites.effects.update()

    ## calculate score
    level.score = round((
      config.score.apex * level.perfect * (config.score.hit - config.score.perfect)
    + config.score.apex * level.hits * config.score.hit
    ) / len(level.chart.notes)
    + level.apex)

    level.scored = util.slide(level.scored, level.score, speed = 2)

  def end(self):
    '''End the level and cleanup resources.'''

    sprites.lanes.empty()
    sprites.notes.empty()
    mixer.music.unload()
    
    game.level = None
    screen.switch = "score"
