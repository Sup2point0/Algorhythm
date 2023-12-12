'''
Implements internal utility functions.
'''

import random
import json

from core import sprites, config
from util.generic import has


def setscore(score, digits: int = None) -> str:
  '''Add zeroes to the front of a value such that it is `digits` long.'''

  points = str(score)
  places = len(points)
  if digits is None:
    digits = len(str(config.score.apex))

  return (f"{'0' * (digits - places)}{score}") if places < digits else points


def randkey(rows: list[str] = None):
  '''Randomly select a key from the non-special game keys.
  
  The row(s) from which the key is selected can be restricted by specifying `rows`.
  '''
  
  def taken(key):
    return has((lane.key for lane in sprites.lanes), key)
  
  if rows is None:
    keys = [key for key in config.keys.rand.keys() if not taken(key)]
  else:
    keys = [
      key for row in rows
      for key in vars(config.keys)[row].keys()
      if not taken(key)
    ]
  
  return random.choice(keys)


def overwrite(file, content: str):
  '''Overwrite a JSON file with `content`.'''

  file.seek(0)
  file.write(json.dumps(content))
  file.truncate()
