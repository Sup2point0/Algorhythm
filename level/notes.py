'''
Note kinds
'''

import random as ran

import pygame as py

from core import level, sprites, screen, config, opt
import util


class Note(py.sprite.Sprite):
  '''A base class from which all notes derive.'''
  
  def __init__(self, lane = None, speed = None, shock = None):
    '''Create a note.
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    | `hit` | `int`, `float` | Beat the note should be hit. |
    | `lane` | `int`, `list[int]` | Starting lane(s) of the note. |
    | `speed` | `float` | How fast the note approaches. Defaults to set speed of difficulty. |
    '''

    super().__init__()

    self.lane = lane
    self.speed = speed
    self.shock = shock  # TODO

  def spawn(self):
    '''Spawn a note.'''

    if hasattr(self.lane, "__iter__"):
      self.lane = ran.choice(self.lane)
    elif not isinstance(self.lane, int):
      self.lane = ran.randint(0, len(sprites.lanes) - 1)
    
    for lane in sprites.lanes:
      if lane.index == self.lane:
        self.lane = lane
        lane.notes.add(self)
        sprites.notes.add(self)
        self.col = vars(opt.col)[util.findrow(lane.key)]
        break

    self.speed = self.speed or config.difficulties[level.chart.difficulty].speed

  def update(self):
    sprites.active.add(self, layer = 2)

    ## process      
    self.rect.topleft = util.root(
      rect = self.rect,
      x = self.lane.cx,
      y = sprites.lines.sprites()[0].rect.y - self.speed * (self.hit - level.beat)
    )
      
    if self.rect.y >= screen.y:
      self.pop()

    ## render
    self.col = vars(opt.col)[util.findrow(self.lane.key)]
    self.image.fill(py.Color(self.col))

  def accuracy(self, beat) -> str | None:
    '''Return accuracy of note hit.'''

    off = abs(self.hit - beat)
    if off < config.difficulties[level.chart.difficulty].perfect:
      return "perfect"
    elif off < config.difficulties[level.chart.difficulty].hit:
      return "hit"
    elif off < config.difficulties[level.chart.difficulty].miss:
      return "miss"
    else:
      return None
    
  def pop(self, acc: str):
    '''Hit note and handle accordingly.'''

    if acc is None:
      return
    
    # First, check if it's a hit, then check if that's a perfect hit.
    if acc != "miss":
      level.hits += 1
      level.chain += 1
      if level.chain >= level.apex:
        level.apex = level.chain
      if acc == "perfect":
        level.perfect += 1
    else:
      level.chain = 0

    self.kill()


class TapNote(Note):
  '''A note hit by a pressed key.'''

  def __init__(self, /, *, hit, **kwargs):
    '''Create a tap note.
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    | `hit` | `int`, `float` | Beat the note should be hit. |
    '''

    super().__init__(**kwargs)

    self.hit = hit

  def spawn(self):
    '''Spawn a tap note.'''

    super().spawn()

    ## render
    self.image = py.Surface([config.lanewidth, 25])
    self.image.fill(py.Color(self.col))
    self.rect = self.image.get_rect()

  def pop(self, hit = False) -> str | None:
    '''Delete the note and return accuracy.
    
    `hit` determines if it was hit by the player.
    '''
    
    acc = self.accuracy(level.beat) if hit else "miss"

    if acc:
      super().pop(acc)

    return acc


class HoldNote(Note):
  '''A note hit by a pressed and held key.'''

  def __init__(self, /, *, hit, hold, **kwargs):
    '''Create a hold note.
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    | `hit` | `int`, `float` | Beat the note should be hit. |
    | `hold` | `int`, `float` | Beat until which the note should be held. |
    '''

    super().__init__(**kwargs)

    self.hit = hit
    self.hold = hold

  def pop(self):
    ''''''

    ...
