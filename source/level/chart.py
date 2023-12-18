'''
Implements the `Chart` class for creating levels.
'''

from core import config, opt

from level.hitline import Hitline
from level.lane import Lane
from level.notes import Note
from level.action import Action


class Chart:
  '''An Algorhythm level.'''

  def __init__(self,
    difficulty,
    speed = None,
    keys = opt.keys,
    back = None,
    data = None,
  ):  # TODO change initialiser to use lane objects
    '''Create a chart.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `difficulty` | `int` | Chart difficulty, indexed from the pre-defined game difficulties. |
    | `lanes` | `int` | Initial number of lanes. |
    | `keys` | `list[str[upper]]` | Initial lanekeys. |
    | `back` | `splash.Asset` | Background image sprite. |
    | `data` | `list[Hitline, Note, Action]` | Chart data, in the form of a list of chart objects. |
    '''

    self.difficulty = difficulty
    self.speed = speed or config.difficulties[difficulty].speed
    self.back = back or ...
    self.lanes = []
    for i, key in enumerate(keys):
      self.lanes.append(Lane(index = i, key = key))
    
    self.data = data or []
    self.lines = [Hitline()]
    self.notes = []
    self.actions = []
    
    for each in data:
      if isinstance(each, Note):
        self.notes.append(each)
      
      elif isinstance(each, Action):
        if each.loops:
          self.actions.extend(each.actions)
        else:
          self.actions.append(each)
      
      elif isinstance(each, Hitline):
        self.lines.append(each)

    self.actions.sort(key = lambda action: action.beat)