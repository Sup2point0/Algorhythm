'''
Implements the innate `Difficulty` and `Rank` classes.

Safe to import.
'''

from innate.object import Object


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


class Achievement(Object):
  '''Represents a game achievement.'''

  def __init__(self,
    id: str,
    name = None,
    desc = None,
    secret = False,
    root = None
  ):
    '''Create an achievement.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `id` | `str` | Unique ID to identify achievement. |
    | `name` | `str` | Displayed name of achievement. |
    | `desc` | `str` | Description of achievement. |
    | `secret` | `bool` | Whether the achievement is secret (hidden until unlocked). |
    | `root` | `Callable -> bool` | Function called to check if achievement should be unlocked. |
    '''

    if root is None:
      raise ValueError("Achievement root is required.")

    super().__init__(
      id = id,
      name = name or "Achievement Unlocked!",
      desc = desc or "How is this unlocked again?",
      secret = secret,
      root = root,
      unlocked = False,
    )
