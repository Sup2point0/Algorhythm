'''
Game difficulties
'''


class Difficulty:
  '''Represents a chart difficulty.'''

  def __init__(self, name, leniency: float, speed):
    '''Create a difficulty.
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    | `name` | `str` | The displayed name of the difficulty. |
    | `leniency` | `float` | The leniency (measured in beats) allowed for a perfect hit. The leniency for any hit is always double this. |
    | `speed` | `int`, `float` | How fast the notes approach. |
    '''

    self.name = name
    self.perfect = leniency
    self.hit = leniency * 2
    self.miss = leniency * 2.5
    self.speed = speed
