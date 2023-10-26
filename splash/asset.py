'''
Implements the `Asset` class, for image sprites.
'''

import pygame as py

from splash.elements import Element
from core import sprites

import effects.blur


class Asset(Element):
  '''An image–only splash element.'''

  def __init__(self, id, pos,
    image: str,
    size = None,
    blur = None,
    display = None,
  ):
    '''Create an image element.

    ｜ parameter | type | description |
    | :--------- | :-- | :----------- |
    | `image` | The file name from which to load the image asset. |
    | `size` | `int, int` | Resize image if specified. |
    | `blur` | Amount of blur to apply to image. |

    Other base parameters are inherited from `splash.Element`.
    '''

    super().__init__(id, pos,
      align = display.align if display else None,
      display = display,
    )

    self.root = py.image.load(f"assets/{image}")
    
    if size:
      self.surf = py.transform.scale(self.root, size)
    if blur:
      self.surf = effects.blur.blur(self.root, blur)
    
    self.surf = self.surf.convert()
    self.rect = self.surf.get_rect()
