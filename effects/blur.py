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
