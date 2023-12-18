'''
Implements the `Track` class for creating levels.
'''

from copy import copy

import pygame as pg
from pygame import mixer

from core import game, level, screen, sprites, config
from innate import Val
import util


class Track:
  '''A particular soundtrack.'''

  def __init__(self, id,
    name,
    file,
    artist = None,
    bpm = None,
    offset = None,
    vol = 1.0,
    charts = None,
  ):
    '''Create a soundtrack.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `id` | `str` | Internal identifier for track, used for finding cover art. |
    | `name` | `str` | Track name. |
    | `artist` | `str` | Track artist. |
    | `file` | `str` | Source file (path) to stream audio from. |
    | `bpm` | `num` | Tempo of track in beats per minute (can be scaled for easier charting). |
    | `offset` | `float` | Time offset to apply to beat calculations. |
    | `vol` | `0.0 < num < 1.0` | Internal volume of soundtrack. |
    | `charts` | `list[Chart]` | Playable charts of track. |
    '''

    self.id = id
    self.name = name
    self.artist = artist
    self.file = f"assets/tracks/{file}"
    self.bpm = bpm# or util.find.sync(self.file)["tempo"]
    self.offset = offset# or util.find.sync(self.file)["offset"]
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

    # load level data into shallow copies to avoid altering original list
    level.data.notes = copy(level.chart.notes)
    level.data.actions = copy(level.chart.actions)

    level.beat = 0
    level.tick = 0
    level.score = 0
    level.scored = 0
    level.hits = 0
    level.perfect = 0
    level.slips = 0
    level.chain = 0
    level.apex = 0

    level.lane.space = config.lane.space

    # clear just to be safe
    sprites.lines = pg.sprite.Group(*level.chart.lines)
    sprites.lanes = pg.sprite.Group(*level.chart.lanes)
    sprites.notes.empty()
    sprites.actions.empty()
    
    pg.key.set_repeat()  # disable keypress repetition when held
    mixer.music.fadeout(1000)
    level.started = False  # only becomes True once music starts

  def run(self):
    '''Process and control chart.'''
    
    level.tick += 1

    ## start or end level
    if not mixer.music.get_busy():
      if not level.started:
        if level.tick > 60:
          mixer.music.load(self.file)
          mixer.music.set_volume(self.vol)
          mixer.music.play()
          level.started = True
      else:
        return self.end()
    
    ## process level
    if level.started:
      level.beat = game.level.bpm * (mixer.music.get_pos() + game.level.offset) / 60000

      # chart elements are removed from the pending processing lists once processed
      for i, note in enumerate(level.data.notes):
        if level.beat >= note.spawnbeat:
          note.spawn()
          level.data.notes.pop(i)
        else:
          break

      for i, action in enumerate(level.data.actions):
        if level.beat >= action.beat:
          action.activate()
          level.data.actions.pop(i)
        else:
          break

    # these updates follow a specific order
    sprites.lines.update()
    sprites.notes.update()
    sprites.lanes.update()
    sprites.actions.update()
    sprites.effects.update()

    ## calculate score
    level.score = round((
      config.score.apex * level.perfect * (config.score.perfect - config.score.hit)
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

    pg.key.set_repeat(*config.rate.key)
