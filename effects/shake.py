'''
Screen shake effects handling

This module does not import any other in-game modules.
'''

import random


class Shake:
  '''A class for handling shake effects in a particular axis.'''

  style = enum("", ["pulse", "flux"])
  '''Shake effect styles.

  | style | description |
  | :---- | :---------- |
  | `pulse` | Shake in a single direction. |
  | `flux` | Rapidly flux between both directions. |
  '''

  def __init__(self, axis: str):
    '''Create a shake effect in a specified `axis`.'''

    self.axis = axis
    self.shake = 0
    self.vect = 0
    self.speed = 1
    self.style = Shake.style.pulse

  def __call__(self):
    return self.vect
    # a nicer way of fetching shake value than something like `screen.shake.x.vect`

  def decay(self):
    '''Update shaking.'''

    if self.shake > 0:
      self.shake -= self.speed
    if self.style == Shake.style.pulse:
      self.vect = self.shake
    elif self.style == Shake.style.flux:
      self.vect = self.shake * random.uniform(-1, 1)
