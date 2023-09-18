'''
Blur effects
'''

import pygame as py
from PIL import Image, ImageFilter


def load(file: str, blur: int) -> py.Surface:
  '''Load and blur a file into a pygame surface.'''

  image = Image.open(file)
  image = image.filter(ImageFilter.GaussianBlur(blur))
  image = py.image.fromstring(image.tobytes(), image.size, image.mode)

  return image


def process(image: py.Surface, blur: int) -> py.Surface:
  '''Blur an existing pygame surface.'''

  ...
