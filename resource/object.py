'''
Implements the generic `Object` class.
'''


class Object:
  '''A generic object with any attributes that can be updated in bulk.'''

  def __init__(self, **attrs):
    '''Create a generic object with attributes passed as keyword arguments.'''

    for each in attrs:
      self.__setattr__(each, kwargs[each])

  def update(self, **attrs):
    '''Update attributes using keyword arguments.'''

    for each in attrs:
      if hasattr(self, each):
        self.__setattr__(each, attrs[each])
