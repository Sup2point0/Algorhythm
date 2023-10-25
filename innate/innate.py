'''
Implements the innate `Difficulty`, `Rank`, `Achievement` classes.

These implement little extra functionality outside of their certain Attributes.

Safe to import.
'''

from innate import Object


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
  '''Represents a rank for a chart depending on how well the player performed.'''

  def __init__(self, name, col = None, req = None):
    '''Create a rank.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `name` | `str` | Displayed name of rank. |
    | `col` | `Color`, `Color, Color` | Colour (solid or gradient) associated with rank. |
    | `req` | `Callable -> bool` | Function called to check if requirement to reach rank has been met. |
    '''

    super().__init__(
      name = name,
      col = col or 0xffffff,
      req = req or (lambda: True),
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
