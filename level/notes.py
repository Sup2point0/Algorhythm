'''
Note kinds
'''

import random

import pygame as py

from core import level, screen, sprites, config, opt
from innate.sprite import Sprite
import util

from effects.pop import PopEffect


class Note(Sprite):
  '''Base class from which all notes derive.'''
  
  def __init__(self, lane = None, speed = None, shock = None):
    '''Create a note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `lane` | `int`, `list[int]` | Starting lane(s) of the note. If a list is provided, it will be randomly chosen from those lanes. |
    | `speed` | `float` | How fast the note approaches. Defaults to set speed of difficulty. |
    '''

    super().__init__(pos = None, align = (0, 1))  # FIXME

    self.lane = lane
    self.speed = speed
    self.shock = shock

  def spawn(self):
    '''Spawn a note.'''

    if hasattr(self.lane, "__iter__"):
      self.lane = random.choice(self.lane)
    elif not isinstance(self.lane, int):
      self.lane = random.randint(0, len(sprites.lanes) - 1)
    
    for lane in sprites.lanes:
      if lane.index == self.lane:
        self.lane = lane
        lane.notes.add(self)
        sprites.notes.add(self)
        self.col = util.find.col(lane.key)
        break

    self.speed = self.speed or config.difficulties[level.chart.difficulty].speed

  def update(self):
    super().show("notes")

    ly = sprites.lines.sprites()[0].y
    self.x = self.lane.x
    self.y = ly - self.speed * (self.hit - level.beat)
    
    if self.y >= screen.y:
      self.pop()

    self.surf.set_alpha(255 * (self.y - ly) / (screen.y - ly))

    super().position()

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
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `int`, `float` | Beat the note should be hit. |
    '''

    super().__init__(**kwargs)

    self.hit = hit

    self.size = [
      config.note.size[0] * opt.note.size(),
      config.note.size[1]
    ]

  def spawn(self):
    '''Spawn a tap note.'''

    super().spawn()

    ## render
    self.surf = py.Surface(self.size, py.SRCALPHA)

    self.surf = ...

    py.draw.rect(
      surface = surf,
      color = py.Color(0xffffffff),
      rect = py.Rect(0, 0, *self.size),
      width = 0,
      border_radius = min(self.size) // 2,
    )
    
    self.rect = self.surf.get_rect()

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
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `int`, `float` | Beat the note should be hit. |
    | `hold` | `int`, `float` | Beat until which the note should be held. |
    '''

    super().__init__(**kwargs)

    self.hit = hit
    self.hold = hold

  def pop(self):
    ''''''

    ...


class RollNote:
  '''...'''

  ...
