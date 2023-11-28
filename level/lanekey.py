'''
Implements the `LaneKey` class for displaying keys for each lane.
'''

import pygame as pg

from core import level, screen, config
from innate import Val
from innate.sprite import Sprite
import util

from splash.text import Text


class LaneKey(Sprite):
  '''A text element beneath each lane indicating its key.'''
  
  def __init__(self, lane):
    '''Create a lane key indicator.'''
    
    super().__init__()
    
    self.lane = lane
    self.key = self.lane.key
    
    self.alpha = util.Alpha(0)
    self.style = Text.Style("title", 69, col = util.find.col(self.key))
    
    class anim:
      size = self.style.size * 10
    
    self.anim = anim
  
  def update(self):
    if not self.lane.alive():
      self.kill()
    else:
      super().show("lanekeys")
  
    ## animate
    if level.tick < 120:
      if level.tick > 15 + self.lane.index * 6:
        self.alpha.alt(4)
        self.anim.size = util.slide(self.anim.size, self.style.size, speed = 5)
    else:
      self.anim.size = util.slide(self.anim.size, self.style.size, speed = 5)
    
    if self.lane.key != self.key:
      self.key = self.lane.key
      self.anim.size = self.style.size * 2
    
    ## render
    self.surf, self.rect = Text.render(
      text = self.lane.key.upper(),
      style = self.style.updated(size = self.anim.size)
    )
    self.surf.set_alpha(self.alpha())
    
    self.x = self.lane.x
    self.y = screen.y - config.lane.space * 2
    super().position()
