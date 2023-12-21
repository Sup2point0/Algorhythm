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

    style = Text.Style(size = 25, col = ui.col.text.idle[:3] + [0])
    self.style = (lambda align: style.updated(align = (align, 0)))

    class layout:
      space = 50
      x3 = [50, 325, 550]
      x4 = [50, 250, 350, 550]

    self.layout = layout
    self.reset()
    
    self.rect = pg.Rect(pos, self.size)
    super().position()

  def reset(self):
    '''Reset animation attributes.'''

    self.anim.state = True
    self.anim.tick = 0

    rects = []
    y = 0
    for height in [80, 160, 600]:
      rects.append(pg.Rect(0, y, 0, height))
      y += height + 20
    self.anim.rects = rects
    
    self.anim.styles = {
      "score": Text.Style(typeface = "title", size = 50, align = (-1, 0)),
      "info": [self.style(-1), self.style(1), self.style(1)],
      "details": [self.style(-1), self.style(1)]
    }

  def update(self):
    self.anim.tick += 1
    self.surf = pg.Surface(self.size, pg.SRCALPHA)

    tick = self.anim.tick
    styles = self.anim.styles

    ## backing rectangles
    if tick > 15:
      self._slide_(0)
      pg.draw.rect(self.surf, ui.col.back, rect = self.anim.rects[0])
    
    if tick > 30:
      self._slide_(1)
      pg.draw.rect(self.surf, ui.col.back, rect = self.anim.rects[1])
    
    if tick > 45:
      self._slide_(2)
      pg.draw.rect(self.surf, ui.col.back, rect = self.anim.rects[2])
      
    ## score
    if tick > 30:
      self._fade_(styles["score"])
      self._render_(styles["score"], level.scored,
        (self.layout.x3[0], self.anim.rects[0].h / 2))

    ## info
    y = self.anim.rects[1].y

    if tick > 45:
      style = styles["info"][0]
      self._fade_(style)
      self._render_(style, "CHAIN",
        (self.layout.x3[0], y + self._space_(1))
      )
      self._render_(style, "PRECISION",
        (self.layout.x3[0], y + self._space_(2))
      )
      self._render_(style, "ACCURACY",
        (self.layout.x3[0], y + self._space_(3))
      )
    
    if tick > 60:
      style = styles["info"][1]
      self._fade_(style)
      self._render_(style, level.apex,
        (self.layout.x3[1], y + self._space_(1))
      )
      self._render_(style, "<PREC>",
        (self.layout.x3[1], y + self._space_(2))
      )
      self._render_(style, "<ACC>",
        (self.layout.x3[1], y + self._space_(3))
      )
    
    if tick > 75:
      style = styles["info"][2]
      self._fade_(style)
      self._render_(style, level.apex,
        (self.layout.x3[2], y + self._space_(1))
      )
      self._render_(style, "<PREC>",
        (self.layout.x3[2], y + self._space_(2))
      )
      self._render_(style, "<ACC>",
        (self.layout.x3[2], y + self._space_(3))
      )

    ## details
    y = self.anim.rects[2].y

    if tick > 60:
      style = styles["details"][0]
      self._fade_(style)
      self._render_(style, "HIT",
        (self.layout.x4[0], y + self._space_(1))
      )
      self._render_(style, "PERFECT",
        (self.layout.x4[0], y + self._space_(2))
      )
      self._render_(style, "FAULTS",
        (self.layout.x4[0], y + self._space_(3))
      )
      self._render_(style, "MISSED",
        (self.layout.x4[0], y + self._space_(4))
      )
      self._render_(style, "EARLY",
        (self.layout.x4[2], y + self._space_(1))
      )
      self._render_(style, "LATE",
        (self.layout.x4[2], y + self._space_(2))
      )
      if game.mode == "expert":
        self._render_(style, "SLIPS",
          (self.layout.x4[2], y + self._space_(3))
        )
        self._render_(style, "FIXED",
          (self.layout.x4[2], y + self._space_(4))
        )

    if tick > 75:
      style = styles["details"][1]
      self._fade_(style)
      self._render_(style, level.hits,
        (self.layout.x4[1], y + self._space_(1))
      )
      self._render_(style, level.perfect,
        (self.layout.x4[1], y + self._space_(2))
      )
      self._render_(style, level.faults,
        (self.layout.x4[1], y + self._space_(3))
      )
      self._render_(style, level.missed,
        (self.layout.x4[1], y + self._space_(4))
      )
      self._render_(style, level.early,
        (self.layout.x4[3], y + self._space_(1))
      )
      self._render_(style, level.late,
        (self.layout.x4[3], y + self._space_(2))
      )
      if game.mode == "expert":
        self._render_(style, level.slips,
          (self.layout.x4[3], y + self._space_(3))
        )
        self._render_(style, level.fixed,
          (self.layout.x4[3], y + self._space_(4))
        )

  def _slide_(self, idx):
    '''Animate backing rectangle.'''

    rect = self.anim.rects[idx]
    rect.w = util.slide(rect.w, self.size[0], speed = 4)

  def _fade_(self, style):
    '''Increase alpha of text style for fade-in animation.'''

    if style.col[3] < 255:
      style.col[3] += config.rate.fade
      if style.col[3] > 255:
        style.col[3] = 255

  def _render_(self, style, text, pos):
    '''Render text to the sprite (has a cleaner argument order).'''

    surf, rect = Text.render(text, style)
    self.surf.blit(surf, dest = util.root(rect, *pos, align = style.align))

  def _space_(self, factor):
    '''Calculate spacing.'''

    return self.layout.space * (factor - 0.4)
