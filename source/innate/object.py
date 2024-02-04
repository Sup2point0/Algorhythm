'''
Implements the generic `Object` class.

Safe to import.

## NOTE pending deprecation?
'''

from copy import deepcopy


class Object:
  '''A generic object with any attributes that can be set and updated in bulk.'''

  def __init__(self, **attrs):
    '''Create a generic object with attributes passed as keyword arguments.'''

    for each in attrs:
      self.__setattr__(each, attrs[each])

  def update(self, **attrs):
    '''Update attributes using keyword arguments.'''

    for each in attrs:
      if hasattr(self, each):
        self.__setattr__(each, attrs[each])

  def updated(self, **attrs):
    '''Return copy of object with updated attributes.'''

    copy = deepcopy(self)
    copy.update(**attrs)
    
    return copy
