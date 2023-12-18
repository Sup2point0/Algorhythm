'''
Implements the `Note` base class for other note classes to derive from.
'''

import random
from typing import Iterable

from core import level, screen, sprites, config
from innate.sprite import Sprite
import util


class Note(Sprite):
  '''Base class from which all notes derive.'''
  
  def __init__(self, hit, lane = None, speed = None, shock = None, **kwargs):
    '''Create a note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `num`, `num, num` | Beat to hit note on. Some note kinds may need a start and stop beat. |
    | `lane` | `int`, `list[int]` | Starting lane(s) of note. If a list is provided, it will be randomly chosen from those lanes. |
    | `speed` | `float` | How fast note approaches. Defaults to set speed of difficulty. |
    | `shock` | `Callable` | Function called when note hit to apply shock effect. |
    '''

    super().__init__(**kwargs)

    self.hit = hit
    self.lane = lane
    self.speed = speed
    self.shock = shock

    self.line = lambda: sprites.lines.sprites()[0].y
    '''Utility method to find y coordinate of hitline.'''

  def spawn(self):
    '''Initialise a note with by linking it to a lane.'''

    if isinstance(self.lane, Iterable):
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

    sprites.notes.add(self)

  def update(self):
    super().show("notes")
    super().position()

  def move(self):
    '''Update note position.'''
    
    self.x = self.lane.x
    self.y = self.line() - self.speed * (self.hit - level.beat)
    
  def out(self):
    '''Handle note vanishing when missed.'''

    if self.y >= screen.y:
      self.pop()
      
    self.surf.set_alpha(255 * (
      1 - (self.y - self.line()) / (screen.y - self.line()))
    )

  def precision(self, beat, hit) -> str | None:
    '''Return precision of note hit.'''

    off = abs(hit - beat)
    window = config.difficulties[level.chart.difficulty]
    if off < window.perfect:
      return "perfect"
    elif off < window.hit:
      return "hit"
    elif off < window.fault:
      return "fault"
    else:
      return None
    
  def pop(self, prec: str):
    '''Hit note and handle accordingly.'''

    if prec is None:
      return
    
    # First, check if it's a hit, then check if that's a perfect hit.
    if prec != "fault":
      level.hits += 1
      level.chain += 1
      if level.chain >= level.apex:
        level.apex = level.chain
      if prec == "perfect":
        level.perfect += 1
    
    else:
      level.slips += 1
      level.chain = 0

    self.kill()

  @ property
  def spawnbeat(self) -> int | float:
    '''Find suitable beat to spawn note.'''

    hit = self.hit[0] if isinstance(self.hit, Iterable) else self.hit
    speed = self.speed or config.difficulties[level.chart.difficulty].speed
    dist = self.line() / speed

    return hit - dist - 1
    # leave a little leeway so the note spawns slightly earlier than appearing onscreen
