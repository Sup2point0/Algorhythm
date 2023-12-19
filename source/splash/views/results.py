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
    self.style = Text.Style(size = 25)
    self.stylescore = Text.Style(typeface = "title", size = 50)

    self.rect = pg.Rect(pos, self.size)

    self.reset()
    super().position()

  def _slide_(self, idx):
    '''...'''

    self.anim.x[idx] = util.slide(self.anim.x[idx], self.size[0], speed = 4)

  def reset(self):
    '''Reset animation attributes.'''

    self.anim.tick = 0
    self.anim.x = [0, 0, 0]
    self.anim.text = [
      {
        "score": 0,
      }, {
        "prec": [0, 0, 0],
        "acc": [0, 0, 0],
        "chain": [0, 0, 0],
      }, {
        "hit":     [0, 0],  "early": [0, 0],
        "perfect": [0, 0],  "late":  [0, 0],
        "fault":   [0, 0],  "slips": [0, 0],
        "missed":  [0, 0],  "fixed": [0, 0],
      }
    ]

  def update(self):
    self.render()

  def render(self):
    ''''''

    self.surf = pg.Surface(self.size, pg.SRCALPHA)

    self.anim.tick += 1

    ## background rectangles
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
      self.surf.blit(Text.render(level.score, self.stylescore)[0], dest = (20, 20))

    ## ...
    if self.anim.tick > 0:
      self.surf.blit(Text.render("CHAIN", self.style)[0], dest = (0, 200))
    if self.anim.tick > 0:
      self.surf.blit(Text.render("PRECISION", self.style)[0], dest = (0, 200))
    if self.anim.tick > 0:
      self.surf.blit(Text.render("ACCURACY", self.style)[0], dest = (0, 200))

    ## breakdown
    if self.anim.tick > 0:
      self.surf.blit(Text.render("HIT", self.style)[0], dest = (0, 200))
    if self.anim.tick > 0:
      self.surf.blit(Text.render("PERFECT", self.style)[0], dest = (0, 200))
    if self.anim.tick > 0:
      self.surf.blit(Text.render("FAULTS", self.style)[0], dest = (0, 200))
    if self.anim.tick > 0:
      self.surf.blit(Text.render("MISSED", self.style)[0], dest = (0, 200))
    if self.anim.tick > 0:
      self.surf.blit(Text.render("EARLY", self.style)[0], dest = (0, 200))
    if self.anim.tick > 0:
      self.surf.blit(Text.render("LATE", self.style)[0], dest = (0, 200))
    if game.mode == "expert":
      if self.anim.tick > 0:
        self.surf.blit(Text.render("SLIPS", self.style)[0], dest = (0, 200))
      if self.anim.tick > 0:
        self.surf.blit(Text.render("FIXED", self.style)[0], dest = (0, 200))
