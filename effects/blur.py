'''
Blur effects
'''

import pygame as py
from PIL import Image, ImageFilter


def _blur_(image, blur) -> py.Surface:
  '''Internal utility function to blur a Pillow image.'''

  out = image.filter(ImageFilter.GaussianBlur(blur))
  out = py.image.fromstring(out.tobytes(), out.size, out.mode)
  return out


def load(file: str, blur: int) -> py.Surface:
  '''Load and blur a file into a pygame surface.'''

  image = Image.open(file)
  return _blur_(image, blur)


def process(surf: py.Surface, blur: int) -> py.Surface:
  '''Blur an existing pygame surface.'''

  image = Image.frombytes("RGBA", surf.get_size(), py.image.tostring(surf, "RGBA"))
  return _blur_(image, blur)


def glow(size, col, blur: int) -> py.Surface:
  '''Generate a blurred solid colour pygame surface for glow effects.
  
  | parameter | type | description |
  | :-------- | :--- | :---------- |
  | `size` | `int, int` | Dimensions of surface. |
  | `col` | `Color` | Color of the glow effect. |
  | `blur` | `int` | Radius of the Gaussian blur to apply. |
  '''

  surf = py.Surface(size)
  surf.fill(py.Color(col))
  return process(surf, blur)
