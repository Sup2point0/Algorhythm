'''
Screen shake effects handling

This module does not import any other in-game modules.
'''

import random
from enum import Enum


class Shake:
  '''A class for handling shake effects in a particular axis.'''

  style = Enum("", ["pulse", "flux"])
  '''Shake effect styles.

  | style | description |
  | :---- | :---------- |
  | `pulse` | Shake in a single direction. |
  | `flux` | Rapidly flux between both directions. |
  '''

  def __init__(self, shake = 0, decay: int = 1, style = Shake.style.pulse):
    '''Create a shake effect in a specified `axis`.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `shake` | `num` | Magnitude to shake by. |
    | `decay` | `num` | How quickly the shake stops. For `shake.pulse`, the higher, the slower; for `shake.flux`, the higher, the faster. |
    | `style` | `Shake.style` | The kind of shake. (See `Shake.style`) |
    '''

    self.shake = shake
    self.vect = 0
    self.decay = decay
    self.style = shake
  
  def __call__(self):
    return self.vect
    # a nicer way of fetching shake value than something like `screen.shake.x.vect`

  def process(self):
    '''Update and decay shaking.'''

    match self.style:
      case Shake.style.pulse:
        self.vect = self.shake
        self.shake = (0 - self.shake) / self.decay
      
      case Shake.style.flux:
        if self.shake > 0:
          self.vect = self.shake * random.uniform(-1, 1)
          self.shake -= self.decay
        else:
          self.vect = 0
          self.shake = 0
