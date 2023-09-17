'''
Text rendering
'''

import pygame as py
from pygame import freetype

from core import sprites, ui
import util

from splash.elements import Element


freetype.init()


class Text(SplashElement):
  '''A static text element.'''

  class Style(Element.Style):
    '''A text style.'''
  
    def __init__(self, *, typeface = None, size = None, col = None, align = None):
      '''Create a text style.

      | parameter | type | description |
      | :-------- | :--- | :---------- |
      | `typeface` | `str` | Name of font file. |
      | `size` | `num` | |
      | `col` | `Color`, `dict` | Either a single text colour, or a dictionary specifying colours for various states. |
      | `align` | `int, int` | Alignment in x and y axes, respectively. `0` for centre, `1` for right / bottom, `-1` for left / top. |
  
      Arguments are set to internal defaults if unspecified.
      '''
  
      self.typeface = typeface or ui.font.body
      self.size = size or ui.font.size
      self.align = align or (0, 0)

      self.cols = vars(ui.col.text)
      if isinstance(col, dict):
        for each in col:
          self.cols[each] = col[each]
        self.col = self.cols["idle"]
      else:
        self.col = col or self.cols["idle"]

  
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
  def render(cls, text, style = Style()) -> tuple[py.Surface, py.Rect]:
    '''Generates a surface and its rect with rendered text.'''

    return freetype.Font(f"assets/fonts/{style.typeface}.ttf", style.size).render(text, style.col)


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
