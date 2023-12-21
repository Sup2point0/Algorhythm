'''
Implements the `LevelResults` class for viewing performance after finishing a level.
'''

import pygame as pg

from core import game, level, ui, config
import util

from splash.elements import Element
from splash.text import Text


class LevelResults(Element):
  '''A collection of splash elements for displaying level results.'''

  def __init__(self, id, pos, display = None):
    '''Create a level results view.
    
    All parameters are base parameters inherited from `splash.Element`.
    '''

    super().__init__(id, pos, anim = True, display = display)

    self.size = ui.size.views.results
    self.style = Text.Style(size = 25,
      col = ui.col.text.idle[:3] + [0],
    )

    self.rect = pg.Rect(pos, self.size)

    class layout:
      left = 50
      space = 25

    self.layout = layout

    self.reset()
    super().position()

  def reset(self):
    '''Reset animation attributes.'''

    self.anim.state = True
    self.anim.tick = 0

    rects = []
    rects.append([0, 0, 0, 100])
    rects.append([0, rects[0].h + 50, 0, 200])
    rects.append([0, rects[1].y + rects[1].h + 50, 0, 600])
    self.anim.rects = rects
    
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
    styles = self.anim.styles
    
    self.surf = pg.Surface(self.size, pg.SRCALPHA)

    ## backing rectangles
    if self.anim.tick > 15:
      self._slide_(0)
      pg.draw.rect(self.surf, ui.col.back, rect = self.anim.rects[0])
    
    if self.anim.tick > 30:
      self._slide_(1)
      pg.draw.rect(self.surf, ui.col.back, rect = self.anim.rects[1])
    
    if self.anim.tick > 45:
      self._slide_(2)
      pg.draw.rect(self.surf, ui.col.back, rect = self.anim.rects[2])
      
    ## score
    if self.anim.tick > 30:
      self._fade_(styles["score"])
      self._render_((20, 20), styles["score"], level.scored)

    ## info
    if self.anim.tick > 45:
      style = styles["info"][0]
      self._fade_(style)
      self._render_((self.layout.left, 175), style, "CHAIN")
      self._render_((self.layout.left, 200), style, "PRECISION")
      self._render_((self.layout.left, 225), style, "ACCURACY")
    if self.anim.tick > 60:
      style = styles["info"][1]
      self._fade_(style)
      self._render_((self.layout.left, 175), style, "CHAIN")
      self._render_((self.layout.left, 200), style, "PRECISION")
      self._render_((self.layout.left, 225), style, "ACCURACY")

    ## details
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
    '''Animate backing rectangle.'''

    rect = self.anim.rects[idx]
    rect.w = util.slide(rect.w, self.size[0], speed = 4)

  def _fade_(self, style):
    '''Increase alpha of text style for fade-in animation.'''

    style.col[3] += config.fade.rate

  def _render_(self, pos, style, text):
    '''Render text to the sprite (has a cleaner argument order).'''

    self.surf.blit(Text.render(text, style)[0], dest = pos)
