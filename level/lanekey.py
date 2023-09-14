'''
Lane key indicators
'''

from core import sprites
import util

from splash.text import Text


class LaneKey(py.sprite.Sprite):
  '''A text element beneath each lane indicating its key.'''
  
  def __init__(self, lane):
    '''Create a lane key indicator.'''
    
    super().__init__()
    
    self.lane = lane
    self.key = self.lane.key
    
    self.alpha = util.Alpha(0)
    self.style = Text.Style(
      typeface = "Orbitron-Semibold",
      size = 20,
      col = util.find.col(self.key),
    )
    
    class anim:
      size = self.style.size * 4
    
    self.anim = anim
  
  def update(self):
    if not self.lane.alive():
      self.kill()
    else:
      sprites.active.add(self, layer = ...)
  
    ## animate
    if level.tick < 600:
      if level.tick > 15 + self.lane.index * 15:
        self.alpha.alt(-4)
        self.anim.size = util.slide(self.anim.size, self.style.size, speed = 10)
    
    else:
      self.anim.size = util.slide(self.anim.size, self.style.size, speed = 5)
    
    if self.lane.key != self.key:
      self.key = self.lane.key
      self.anim.size = self.style.size * 2
    
    ## render
    self.image, self.rect = Text.render(
      text = self.lane.key.upper(),
      style = Text.Style(
        typeface = "Orbitron-Semibold",
        size = self.anim.size,
        col = util.find.col(self.key),
      )
    )
    
    self.rect.topleft = util.root(self.rect,
      x = self.lane.x,
      y = screen.y - config.lanespace * 2,
    )
