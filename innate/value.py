'''
Implements the `BoundValue` class for values restricted within certain bounds.

Safe to import.
'''


class BoundValue:
  '''Represents a value restricted between 2 bounds.
  
  The value can be quickly returned by calling the object. The value should be changed with the `.set()` and `.alt()` methods to avoid going out of the bounds.
  '''

  def __init__(self, value, lower = None, upper = None):
    '''Create a bound value of any type that supports addition, and inequality comparisons.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `value` | `num`, `Any` | Initial value. |
    | `lower` | `num`, `Any` | Lower bound of value. |
    | `upper` | `num`, `Any` | Upper bound of value. |

    Setting the value to `'lower'` or `'upper'` sets it to the value for that bound. If a bound(s) is unspecified, the value will not be restricted in that direction.
    '''

    self.lower = lower
    self.upper = upper

    if (lower, upper) != (None, None):
      if lower > upper:
        raise ValueError("Lower bound cannot be greater than upper bound")
    
    if value == "lower":
      self.value = self.lower
    elif value == "upper":
      self.value = self.upper
    else:
      self.value = value

    self._check_()
  
  def _check_(self):
    '''Internal method to ensure value is within bounds.'''

    if self.lower is not None:
      if self.value < self.lower:
        self.value = self.lower
    
    if self.upper is not None:
      if self.value > self.upper:
        self.value = self.upper

  def __call__(self):
    '''A more convenient way to get the value than `BoundValue().value`.'''

    return self.value

  def set(self, value, /):
    '''Set the value.'''

    self.value = value
    self._check_()

  def alt(self, value, /):
    '''Alter the value.'''

    self.value += value
    self._check_()

  def bounded(self) -> bool:
    '''Check if value is at a bound.'''

    return self.value in {self.lower, self.upper}
