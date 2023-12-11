'''
Implements the `blur` and `glow` functions for effects involving blurring.
'''

import pygame as pg
from PIL import Image, ImageFilter


def _image_(surf) -> Image.Image:
  '''Internal utility function to convert a pygame Surface to a Pillow image.'''

  return Image.frombytes("RGBA", surf.get_size(), pg.image.tostring(surf, "RGBA"))

def _blur_(image, blur) -> pg.Surface:
  '''Internal utility function to blur a Pillow image.'''

  out = image.filter(ImageFilter.GaussianBlur(blur))
  out = pg.image.fromstring(out.tobytes(), out.size, out.mode)
  return out


def blur(surf: pg.Surface, blur: int) -> pg.Surface:
  '''Blur an existing pygame surface.'''

  return _blur_(_image_(surf), blur)


def glow(size, dist, col, blur: int) -> pg.Surface:
  '''Generate a blurred solid colour pygame surface for glow effects.
  
  | parameter | type | description |
  | :-------- | :--- | :---------- |
  | `size` | `num, num` | Dimensions of surface. |
  | `dist` | `num` | ... |
  | `col` | `Color` | Color of the glow effect. |
  | `blur` | `int` | Radius of the Gaussian blur to apply. |
  '''

  base = Image.new("RGBA", (
    round(size[0] + 2 * dist),
    round(size[1] + 2 * dist),
  ), (255, 255, 255, 0))

  surf = pg.Surface(size)
  surf.fill(pg.Color(col))
  image = _image_(surf)
  
  base.paste(image, (dist, dist))

  return _blur_(base, blur)
