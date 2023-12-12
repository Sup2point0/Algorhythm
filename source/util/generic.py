'''
Implements generic utility functions.
'''


def has(iterable, *values, every = False) -> bool:
  '''Check if `iterable` contains any of `values`.
  
  If `every` is `True`, it must contain every specified value.
  '''

  out = (each in iterable for each in values)
  return all(out) if every else any(out)


def log(**attrs):
  '''Adds the specified attributes to a given function. Used as a decorator.'''

  def wrapper(func):
    def root(*args, **kwargs):
      func(*args, **kwargs)

    for each in attrs:
      root.__setattr__(each, attrs[each])

    return root

  return wrapper
