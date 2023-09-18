'''
Blur effects
'''

import pygame as py
import PIL as pil


def load(file: str, blur: int) -> py.Surface:
  '''Load and blur a file into a pygame surface.'''

  image = pil.Image.open(file)
  image = image.filter(pil.ImageFilter.GaussianBlur(blur))
  image = py.image.fromstring(image.tobytes(), image.size, image.mode)

  return image


def process(image: py.Surface, blur: int) -> py.Surface:
  '''Blur an existing pygame surface.'''

  ...
