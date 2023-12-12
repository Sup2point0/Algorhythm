'''
Implements utility functions involving linear interpolation.
'''

import colorsys


def val(start, stop, percent: float = 0.5):
  '''Interpolate any value between 2 endpoints.'''

  return start + percent * (stop - start)


def col(start, stop, percent: float = 0.5):
  '''Interpolate between 2 colours. Alpha is not taken into account.'''

  lower = colorsys.rgb_to_hsv(*start[:3])
  upper = colorsys.rgb_to_hsv(*stop[:3])

  return colorsys.hsv_to_rgb(
    lower[0] + percent * (upper[0] - lower[0]),
    lower[1] + percent * (upper[1] - lower[1]),
    lower[2] + percent * (upper[2] - lower[2]),
  )
