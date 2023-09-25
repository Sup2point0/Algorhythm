'''
Image assets
'''

import pygame as py

from splash.elements import Element
from core import sprites

import effects.blur


class Asset(Element):
  '''An image asset.'''

  def __init__(self, id, pos, image: str, size = None, blur = None, display = None):
    '''Create an image asset.

    ｜ parameter | type | description |
    | :--------- | :-- | :----------- |
    | `image` | The file name from which to load the image asset. |
    | `size` | `[int, int]` | Resize image if specified. |

    Other base parameters are inherited from `splash.Element`.
    '''

    super().__init__(id, pos, display = display)

    if blur:
      self.surf = effects.blur.load(f"assets/{image}", blur = blur)
    else:
      self.surf = py.image.load(f"assets/{image}")
    
    if size:
      self.surf = py.transform.scale(self.surf, size).convert()
      
    self.rect = self.surf.get_rect()

  def update(self):
    super().visible()

    ## TODO
