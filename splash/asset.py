'''
Image assets
'''


import pygame as py

from splash.element import Element
from core import sprites


class Asset(Element):
  '''An image asset.'''

  def __init__(self, id, pos, image: str, display = list()):
    '''Create an image asset.'''

    super().__init__(sprites.splash)

    self.image = py.image.load(f"assets/{image}").convert()
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = pos

    self.id = id
    self.display = display

  def update(self):
    self.visible()

    ## TODO
