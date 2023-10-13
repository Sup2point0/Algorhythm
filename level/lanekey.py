'''
Lane key indicators
'''

import pygame as py

from core import level, screen, sprites, config
from innate.sprite import Sprite
import util

from splash.text import Text


class LaneKey(Sprite):
  '''A text element beneath each lane indicating its key.'''
  
  def __init__(self, lane):
    '''Create a lane key indicator.'''
    
    super().__init__()  # FIXME?
    
    self.lane = lane
    self.key = self.lane.key
    
    self.alpha = util.Alpha(0)
    self.style = Text.Style(
      typeface = "Orbitron-Semibold",
      size = 69,
      col = util.find.col(self.key),
    )
    
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
      style = Text.Style(
        typeface = "Orbitron-Semibold",
        size = self.anim.size,
        col = util.find.col(self.key),
      )
    )

    self.surf.set_alpha(self.alpha.value)
    self.x = self.lane.x
    self.y = screen.y - config.lanespace * 2

    super().position()
