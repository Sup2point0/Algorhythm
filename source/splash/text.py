'''
Implements the `Text`, `Textbox`, `ActiveText` classes for displaying text.
'''

import pygame as pg
from pygame import freetype

from core import ui
import util

from splash.elements import Element


freetype.init()


class Text(Element):
  '''A static text element.'''

  class Style(Element.Style):
    '''A text style.'''
  
    def __init__(self, typeface = None, size = None, col = None, align = None):
      '''Create a text style.

      | parameter | type | description |
      | :-------- | :--- | :---------- |
      | `typeface` | `str` | Name of font file. |
      | `size` | `num` | |
      | `col` | `Color`, `dict` | Either a single text colour, or a dictionary specifying colours for various states. |
      | `align` | `int, int` | Alignment in x and y axes, respectively. `0` for centre, `1` for right / bottom, `-1` for left / top. |
  
      Arguments are set to internal defaults if unspecified.
      '''

      # Check if typeface is a generic, like 'body'
      try:
        typeface = vars(ui.font)[typeface]
      except KeyError:
        pass
  
      self.typeface = typeface or ui.font.body
      self.size = size or ui.size.font
      self.align = align or (0, 0)

      if isinstance(col, dict):
        self._config_cols_(col, ui.col.text)
      else:
        self._config_cols_(None, ui.col.text)
        self.col = col or self.cols["idle"]

  
  def __init__(self, id, pos, text, style = None, display = None):
    '''Create a text element.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `text` | `str` | Text to display. |
    | `style` | `Text.Style` | Style settings for text. |

    Other base parameters are inherited from `splash.Element`.
    '''

    super().__init__(id, pos, display = display)

    self.text = text
    self.style = style or Text.Style()
    
    self.surf, self.rect = Text.render(self.text, self.style)
    super().position()

    if self.display:
      if self.display.scroll:
        self.update = super().position

  @ staticmethod
  def render(text, style = Style()) -> tuple[pg.Surface, pg.Rect]:
    '''Generates a surface and its rect with rendered text.'''

    return freetype.Font(f"assets/fonts/{style.typeface}.ttf", style.size).render(str(text), style.col)


class Textbox(Element):
  '''A block of text spanning multiple lines.'''

  class Style(Text.Style):
    '''A textbox style.'''

    def __init__(self, *args, **kwargs):
      '''Create a textbox style.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    '''

      super().__init__(*args, **kwargs)

      self.space = kwargs.get("space", ui.space.text)


  def __init__(self, id, pos, text, style = None, display = None):
    '''Create a text box.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    '''

    super().__init__(id, pos, display = display)

    self.text = text
    self.style = style or Textbox.Style()

    self._render_()

    if self.display:
      if self.display.scroll:
        self.update = super().position

  def _render_(self):
    self.surfs = [Text.render(each, self.style) for each in self.text]

    # Double iteration is painful, but I can’t (yet) see a better way to do it.
    width = 0
    height = 0
    for surf, rect in self.surfs:
      w, h = surf.get_size()
      height += h + self.style.space
      if w > width:
        width = w
    self.surf = pg.Surface((width, height), pg.SRCALPHA)

    dy = 0
    for surf, rect in self.surfs:
      self.surf.blit(surf, (util.root(rect,
        x = width / 2,
        y = dy + rect.height / 2
      )))
      dy += rect.height + self.style.space

    self.rect = self.surf.get_rect()


class ActiveText(Text):
  '''A dynamic text element that can change the text it displays or where it is positioned.'''

  def __init__(self, id, pos = None, place = None, text = None, source = None, *args, **kwargs):
    '''Create a dynamic text element.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `place` | `Callable` | Function called to fetch text position. |
    | `source` | `Callable` | Function called to fetch displayed text. |

    Other base parameters are inherited from `splash.Text` and `splash.Element`.
    '''

    self.place = place
    self.source = source

    super().__init__(id,
      pos = place() if place else pos,
      text = source() if source else text,
      *args, **kwargs
    )

  def update(self):
    if self.place:
      self.x, self.y = self.place()
    if self.source:
      self.surf, self.rect = Text.render(text = self.source(), style = self.style)

    super().position()
