'''
Implements the `BoundValue` class for values restricted within certain bounds.

This module does not import any in-game modules.
'''


class BoundValue:
  '''Represents a value restricted between 2 bounds.'''

  def __init__(self, value, lower = 0, upper = None):
    '''Create a bound value.

    ...
    '''

    self.value = value
    self.lower = lower
    self.upper = upper
