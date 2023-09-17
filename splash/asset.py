'''
Image assets
'''

import pygame as py

from splash.elements import Element
from core import sprites


class Asset(SplashElement):
  '''An image asset.'''

  def __init__(self, id, pos, image: str, size = None, display = None):
    '''Create an image asset.

    ｜ parameter | type | description |
    | :--------- | :-- | :----------- |
    | `image` | The file name from which to load the image asset. |
    | `size` | `[int, int]` | Resize image if specified. |

    Other base parameters are inherited from `splash.Element`.
    '''

    super().__init__(id, pos, display = display, groups = [sprites.splash])

    self.image = py.image.load(f"assets/{image}").convert()
    if size:
      self.image = py.transform.scale(self.image, size)
      
    self.rect = self.image.get_rect()

  def update(self):
    super().visible()

    ## TODO
