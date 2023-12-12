'''
Implements the `Asset` class, for image sprites.
'''

import pygame as pg

from innate import Alpha

from splash.elements import Element

import effects.blur


class Asset(Element):
  '''An image–only splash element.'''

  def __init__(self, id, pos,
    image: str,
    size = None,
    blur = None,
    dark = None,
    display = None,
  ):
    '''Create an image element.

    ｜ parameter | type | description |
    | :--------- | :-- | :----------- |
    | `image` | The file name from which to load the image asset. |
    | `size` | `int, int` | Resize image if specified. |
    | `blur` | Amount of blur to apply to image. |
    | `dark` | Alpha value of dark cover to overlay on image. |

    Other base parameters are inherited from `splash.Element`.
    '''

    super().__init__(id, pos, display = display)

    self.surf = pg.image.load(f"assets/{image}")
    if size:
      self.surf = pg.transform.scale(self.surf, size)
    if blur:
      self.surf = effects.blur.blur(self.surf, blur)
    self.surf = self.surf.convert()

    if dark is not None:
      self.cover = pg.Surface(self.surf.get_size())
      self.cover.fill(0x000000)
      self.cover.set_alpha(Alpha(dark)())
      self.surf.blit(self.cover, (0, 0))

    self.rect = self.surf.get_rect()
