'''
Implements the `Note` base class for other note classes to derive from.
'''

import random

from core import level, screen, sprites, config
from innate.sprite import Sprite
import util


class Note(Sprite):
  '''Base class from which all notes derive.'''
  
  def __init__(self, lane = None, speed = None, shock = None):
    '''Create a note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `lane` | `int`, `list[int]` | Starting lane(s) of note. If a list is provided, it will be randomly chosen from those lanes. |
    | `speed` | `float` | How fast note approaches. Defaults to set speed of difficulty. |
    | `shock` | `Callable` | Function called when note hit to apply shock effect. |
    '''

    super().__init__()

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

  def update(self, fade = True):
    super().show("notes")

    ly = sprites.lines.sprites()[0].y
    self.x = self.lane.x
    self.y = ly - self.speed * (self.hit - level.beat)
    
    if self.y >= screen.y:
      self.pop()

    if fade:
      self.surf.set_alpha(255 * (1 - (self.y - ly) / (screen.y - ly)))

    super().position()

  def accuracy(self, beat, hit) -> str | None:
    '''Return accuracy of note hit.'''

    off = abs(hit - beat)
    window = config.difficulties[level.chart.difficulty]
    if off < window.perfect:
      return "perfect"
    elif off < window.hit:
      return "hit"
    elif off < window.miss:
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
      level.slips += 1
      level.chain = 0

    self.kill()