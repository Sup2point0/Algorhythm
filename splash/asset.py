'''
Image assets
'''

import pygame as py

from splash.elements import Element
from core import sprites


class Asset(Element):
  '''An image asset.'''

  def __init__(self, id, pos, image: str, display = None):
    '''Create an image asset.

    ｜ parameter | type | description |
    | :--------- | :-- | :----------- |
    | `image` | The file name from which to load the image asset. |

    Other base parameters are inherited from `splash.Element`.
    '''

    super().__init__(id, pos, display = display, groups = [sprites.splash])

    self.image = py.image.load(f"assets/{image}").convert()
    self.rect = self.image.get_rect()

  def update(self):
    super().visible()

    ## TODO
