'''
Implements the `Chart` and `Track` classes for creating levels.
'''

import pygame as py
from pygame import mixer

from core import game, level, screen, sprites, config, opt
from innate import Val
import util

from level.hitline import Hitline
from level.lane import Lane
from level.notes import Note
from level.action import Action


class Chart:
  '''An Algorhythm level.'''

  def __init__(self,
    difficulty: int,
    lanes = 4,
    keys = opt.keys,
    data = None,
  ):  # TODO change initialiser to use lane objects
    '''Create a chart.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `difficulty` | `int` | Chart difficulty, indexed from the pre-defined game difficulties. |
    | `lanes` | `int` | Initial number of lanes. |
    | `keys` | `list[str[upper]]` | Initial lanekeys. |
    | `data` | `list[Hitline, Note, Action]` | Chart data, in the form of a list of chart objects. |
    '''

    self.difficulty = difficulty
    self.lanes = []
    for i in range(lanes):
      self.lanes.append(Lane(index = i, key = keys[i]))
    
    self.data = data or []
    self.lines = [Hitline()]
    self.notes = []
    self.actions = []
    
    for each in data:
      if isinstance(each, Note):
        self.notes.append(each)
      elif isinstance(each, Action):
        self.actions.append(each)
      elif isinstance(each, Hitline):
        self.lines.append(each)


class Track:
  '''A particular soundtrack.'''

  def __init__(self, id,
    name,
    bpm,
    file: str,
    offset: float,
    vol: float = 1.0,
    artist = None,
    charts: list = None,
  ):
    '''Create a soundtrack.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `id` | `str` | Internal identifier for track, used for finding cover art. |
    | `name` | `str` | Track name. |
    | `artist` | `str` | Track artist. |
    | `bpm` | `num` | Tempo of track in beats per minute (can be scaled for easier charting). |
    | `file` | `str` | Source file (path) to stream from. |
    | `offset` | `float` | Time offset to apply to beat calculations. |
    | `vol` | `float in [0.0, 1.0]` | Internal volume of soundtrack. |
    | `charts` | `list[Chart]` | Playable charts of track. |
    '''

    self.id = id
    self.name = name
    self.artist = artist
    self.bpm = bpm
    self.file = file
    self.offset = offset
    self.vol = Val(vol, lower = 0.0, upper = 1.0)()
    self.charts = sorted(charts, key = lambda chart: chart.difficulty) or []
    self.difficulties = (chart.difficulty for chart in self.charts)
    self.cover = util.find.asset(f"covers/{id}.jpeg", "covers/none.png")

  def __getitem__(self, difficulty):
    '''A convenient way to get a particular chart with the specified difficulty.'''

    for chart in self.charts:
      if chart.difficulty == difficulty:
        return chart
    else:
      return None  # if chart not found, return no value and handle accordingly

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
    level.lane.space = config.lane.space

    # clear just to be safe
    sprites.lines = py.sprite.Group(*level.chart.lines)
    sprites.lanes = py.sprite.Group(*level.chart.lanes)
    sprites.actions.empty()
    
    sprites.notes.empty()  # FIXME
    for note in level.chart.notes:
      note.spawn()
      sprites.notes.add(note)
    
    mixer.music.fadeout(1000)
    level.started = False  # only becomes True once music starts

    py.key.set_repeat()  # disable keypress repetition when held

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

      for action in level.chart.actions:
        if level.beat > action.beat:
          action.activate()

    # These updates follow a specific order.
    sprites.lines.update()
    sprites.notes.update()
    sprites.lanes.update()
    sprites.actions.update()
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

    py.key.set_repeat(config.rate.keys)
