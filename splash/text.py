'''
Text rendering
'''

import pygame as py
from pygame import freetype

from splash.element import Element
from core import sprites, ui
import util


freetype.init()


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


class Text(Element):
  '''A static text element.'''

  def __init__(self, id, pos, text, display = list(), style = Style()):
    '''Create a text element.
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    | `id` | | Unique attribute to identify text element. |
    | `pos` | `[int, int]` | Coordinate where text element is positioned. |
    | `text` | `str` | Text to display. |
    | `display` | `list[str]` | List of screen states where button will be shown. |
    | `style` | `splash.text.Style` | Dictionary of style settings for text. |
    '''

    super().__init__(sprites.splash)

    self.pos = pos
    self.text = text
    self.style = style
    
    if self.text:
      self.image, self.rect = Text.render(text = self.text, style = self.style)

    self.id = id
    self.display = display

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
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    | `id` | | Unique attribute to identify text element. |
    | `pos` | `[int, int]` | Coordinate where text element is positioned. |
    | `source` | `Callable` | Function to call to fetch text to display. |
    | `display` | `list[str]` | List of screen states where button will be shown. |
    | `style` | `splash.text.Style` | Dictionary of style settings for text. |
    '''

    self.source = source

    super().__init__(id = id, pos = pos, text = None, *args, **kwargs)

  def update(self):
    self.image, self.rect = Text.render(text = self.source(), style = self.style)

    super().update()
