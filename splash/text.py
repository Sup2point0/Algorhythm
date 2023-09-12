'''
Text rendering
'''

import pygame as py
from pygame import freetype

from core import sprites, ui
import util

from splash.elements import Element


freetype.init()


class Text(Element):
  '''A static text element.'''

  class Style:
    '''A text style.'''
  
    def __init__(self, *, typeface = None, size = None, col = None, align = None):
      '''Create a text style.
  
      Arguments are set to internal defaults if unspecified.
  
      `align` should be a tuple of 2 `int`s, representing x and y alignment, respectively. `0` for centre, `1` for right / bottom, `-1` for left / top.
      '''
  
      self.typeface = typeface or ui.font.typeface
      self.size = size or ui.font.size
      self.col = col or ui.col.text
      self.align = align or (0, 0)

  
  def __init__(self, id, pos, text, style = None, display = None):
    '''Create a text element.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `text` | `str` | Text to display. |
    | `style` | `Text.Style` | Style settings for text. |

    Other base parameters are inherited from `splash.Element`.
    '''

    super().__init__(id, pos, display = display, groups = [sprites.splash])

    self.text = text
    self.style = style or Text.Style()
    
    self.image, self.rect = Text.render(text = self.text, style = self.style)

  def update(self):
    self.visible()
    
    self.rect.x, self.rect.y = util.root(self.rect, *self.pos, align = self.style.align)

  @ classmethod
  def render(cls, text, style = Style()) -> (py.Surface, py.Rect):
    '''Generates a surface and its rect with rendered text.'''

    return freetype.Font(f"assets/{style.typeface}.ttf", style.size).render(text, style.col)


class ActiveText(Text):
  '''A dynamic text element that can change the text it displays.'''

  def __init__(self, id, pos, source, *args, **kwargs):
    '''Create a dynamic text element.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `source` | `Callable` | Function called to fetch displayed text. |

    Other base parameters are inherited from `splash.Text` and `splash.Element`.
    '''

    self.source = source

    super().__init__(id, pos, text = None, *args, **kwargs)

  def update(self):
    self.image, self.rect = Text.render(text = self.source(), style = self.style)

    super().update()
