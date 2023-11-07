'''
Implements the `TapNote`, `HoldNote`, `RideNote`, `RollNote`, `BreakNote` note kinds.
'''

import random

import pygame as py

from core import level, screen, sprites, config, opt
from innate.sprite import Sprite
import util

from effects import blur
from effects.pop import PopEffect


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

    super().__init__(pos = None)

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

    if isinstance(self, TapNote) or isinstance(self, RideNote):
      self.surf.set_alpha(255 * (1 - (self.y - ly) / (screen.y - ly)))

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

  def __init__(self, hit, **kwargs):
    '''Create a tap note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `num` | Beat note should be hit on. |

    Other base parameters are inherited from `Note`.
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
    self.surf = blur.glow(
      size = self.size,
      dist = 50,
      col = self.col,
      blur = 40,
    )

    py.draw.rect(
      surface = self.surf,
      color = py.Color(0xffffffff),
      rect = py.Rect(50, 50, *self.size),
      width = 0,
      border_radius = round(min(self.size) // 2),
    )
    
    self.rect = self.surf.get_rect()

  def pop(self, hit = False) -> str | None:
    '''Delete the note and return accuracy.
    
    `hit` determines if it was hit by the player.
    '''
    
    acc = self.accuracy(level.beat) if hit else "miss"

    if acc:
      super().pop(acc)
      if acc != "miss":
        PopEffect(pos = self.pos, acc = acc)

    return acc


class HoldNote(Note):
  '''A note hit by a pressed and held key.'''

  def __init__(self, hit, **kwargs):
    '''Create a hold note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `num, num` | Beat note should be hit on, and beat it should be held until. |

    Other base parameters are inherited from `Note`.
    '''

    super().__init__(**kwargs)

    self.hit = hit
    if hit[0] >= hit[1]:
      raise ValueError("hold note cannot end before it starts")

  def pop(self):
    ''''''

    ...


class RideNote:
  '''A note hit by a pressed or held key.'''

  def __init__(self, hit, **kwargs):
    '''Create a ride note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `num` | Beat note should be hit on. |

    Other base parameters are inherited from `Note`.
    '''

    super().__init__(**kwargs)

    self.hit = hit

    self.size = [
      config.note.size[0] * opt.note.size() * 0.75,
      config.note.size[1]
    ]


def Rides(lane, hit) -> list[RideNote]:
  '''Utility function to create several ride notes in the same lane at once.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `lane` | `int` | Starting lane of notes. |
    | `hit` | `list`, `range` | Hit beats for each note. This determines how many notes are created. |
    '''
  
  out = []
  for each in hit:
    out.append(RideNote(hit = each, lane = lane))

  return out


class RollNote:
  '''A note hit by multiple key presses.'''

  def __init__(self, hit, hits, **kwargs):
    '''Create a roll note.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `hit` | `num, num` | Beats at which note reaches and passes the hitline, respectively. |
    | `hits` | `int` | Number of hits required to clear note. |

    Other base parameters are inherited from `Note`.
    '''
    
    if hit[0] >= hit[1]:
      raise ValueError("roll note cannot end before it starts")

    self.hit = hit
    self.hits = hits
