'''
Implements the innate `Difficulty` and `Rank` classes.

Safe to import.
'''

from resource.object import Object


class Difficulty(Object):
  '''Represents a chart difficulty.'''

  def __init__(self, name, leniency: float, speed):
    '''Create a difficulty.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `name` | `str` | Displayed name of the difficulty. |
    | `leniency` | `float` | The leniency (measured in beats) allowed for a perfect hit. The leniency for an imperfect hit is always double this. |
    | `speed` | `num` | How fast notes approach. |
    '''

    super().__init__(
      name = name,
      perfect = leniency,
      hit = leniency * 2,
      miss = leniency * 2.5,
      speed = speed,
    )


class Rank(Object):
  '''Represents a rank for a level score.'''

  def __init__(self, name, score, req = None):
    '''Create a rank.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `name` | `str` | Displayed name of rank. |
    | `score` | `int` | Score requirement to reach rank. |
    | `req` | `Callable -> bool` | Function called to check if rank has been reached (for special conditions). |
    '''

    super().__init__(
      name = name,
      score = score,
      req = req,
    )
