'''
Implements the `LevelResults` class for viewing performance after finishing a level.
'''

import pygame as pg

from core import game, level, ui
import util

from splash.elements import Element
from splash.text import Text


class LevelResults(Element):
  '''A collection of splash elements for displaying level results.'''

  def __init__(self, id, pos, display = None):
    '''Create a level results view.'''

    super().__init__(id, pos, anim = True, display = display)

    self.size = ui.size.views.results
    self.style = Text.Style(size = 25,
      col = ui.col.text.idle[:3] + (0,),
    )

    self.rect = pg.Rect(pos, self.size)

    self.reset()
    super().position()

  def reset(self):
    '''Reset animation attributes.'''

    self.anim.state = True
    self.anim.tick = 0

    self.anim.x = [0, 0, 0]
    '''Width of 3 backing rectangles.'''
    
    self.anim.styles = {
      "score": Text.Style(typeface = "title", size = 50),
      "info": [
        self.style, self.style,
        self.style.updated(align = (1, 0)),
      ],
      "details": [self.style, self.style]
    }
    '''Style settings for all text elements.'''

  def update(self):
    self.anim.tick += 1
    
    self.surf = pg.Surface(self.size, pg.SRCALPHA)

    ## backing rectangles
    if self.anim.tick > 15:
      self._slide_(0)
      pg.draw.rect(self.surf, ui.col.back, rect = (0, 0, self.anim.x[0], 100))
    
    if self.anim.tick > 30:
      self._slide_(1)
      pg.draw.rect(self.surf, ui.col.back, rect = (0, 150, self.anim.x[1], 200))
    
    if self.anim.tick > 45:
      self._slide_(2)
      pg.draw.rect(self.surf, ui.col.back, rect = (0, 400, self.anim.x[2], 600))

    ## score
    if self.anim.tick > 120:
      ...
      self.surf.blit(Text.render(level.score, self.anim.styles["score"])[0], dest = (20, 20))

    ## ...
    if self.anim.tick > 0:
      self._render_("CHAIN", (0, 200))
    if self.anim.tick > 0:
      self._render_("PRECISION", (0, 200))
    if self.anim.tick > 0:
      self._render_("ACCURACY", (0, 200))

    ## breakdown
    if self.anim.tick > 0:
      self._render_("HIT", (0, 200))
    if self.anim.tick > 0:
      self._render_("PERFECT", (0, 200))
    if self.anim.tick > 0:
      self._render_("FAULTS", (0, 200))
    if self.anim.tick > 0:
      self._render_("MISSED", (0, 200))
    if self.anim.tick > 0:
      self._render_("EARLY", (0, 200))
    if self.anim.tick > 0:
      self._render_("LATE", (0, 200))
    if game.mode == "expert":
      if self.anim.tick > 0:
        self._render_("SLIPS", (0, 200))
      if self.anim.tick > 0:
        self._render_("FIXED", (0, 200))

  def _slide_(self, idx):
    '''Utility function for animating backing rectangles.'''

    self.anim.x[idx] = util.slide(self.anim.x[idx], self.size[0], speed = 4)

  def _render_(self, tick, text, pos, style):
    '''Utility function to render text to the sprite.'''

    if self.anim.tick > tick:
      style.col
      self.surf.blit(Text.render(text, style)[0], dest = pos)
