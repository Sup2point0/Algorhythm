'''
Buttons
'''

import pygame as py

from splash.element import Element
from core import sprites, ui
import util

from splash import text


class Style:
  '''A button style.'''

  def __init__(self, col: dict = None, edge = "round"):
    '''Create a button style.
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    | `col` | `dict` | The colours for the different states of the button. |
    | `edge` | `str` | Edge style – can be `round`, `sharp` or `angular`. |
    '''

    cols = col or {}

    class states:
      idle = cols["idle"] if "idle" in cols else ui.col.button.idle
      hover = cols["hover"] if "hover" in cols else ui.col.button.hover
      click = cols["click"] if "click" in cols else ui.col.button.click
      click = cols["lock"] if "lock" in cols else ui.col.button.lock
      
    self.col = states

    self.edge = edge


class Button(Element):
  '''A clickable button.'''

  def __init__(self, id, pos, size, text, root, display = list(), style = Style()):
    '''Create a clickable button.
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    | `id` | | Unique attribute to identify button. |
    | `pos` | `[int, int]` | Coordinate where button is positioned. |
    | `size` | `[int, int]` | Dimensions of button. |
    | `text` | `str` | Text to display on button. |
    | `root` | `Callable` | Function to call when button is clicked. |
    | `display` | `list[str]`, `dict[str, bool]` | List of screen states where button will be shown, or a dictionary specifying which screen states to hide on. |
    | `style` | `splash.buttons.Style` | Dictionary of style settings for button. |
    '''

    super().__init__(id = id, pos = pos, display = display, groups = [sprites.splash])

    self.size = size
    self.text = text
    self.root = root
    self.style = style

    self.hover = False
    self.click = False

  def update(self):
    super().visible()
    
    self.image = py.Surface(self.size, py.SRCALPHA)
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = util.root(self.rect, *self.pos)
    
    ## hover and click
    down = any(py.mouse.get_pressed())
    if self.rect.collidepoint(py.mouse.get_pos()):
      if not down:  # hovered
        if self.click:  # clicked and released
          self.root()
        self.hover = True
        self.click = False
        col = self.style.col.hover
      
      elif down and self.hover:  # clicked
        self.click = True
        col = self.style.col.click

      else:
        col = self.style.col.idle
    
    else:  # not hovering
      self.hover = False
      self.click = False
      col = self.style.col.idle
    
    ## render button
    py.draw.rect(
      surface = self.image,
      color = py.Color(col),
      rect = py.Rect(0, 0, *self.size),
      width = 0,
      border_radius = min(self.size) // 3,  # FIXME value
    )
    
    rendered = text.Text.render(
      text = self.text,
      style = text.Style(col = self.style.col.idle if self.hover else None)
    )
    self.image.blit(
      source = rendered[0],
      dest = util.root(
        rect = rendered[1],
        x = self.size[0] / 2,
        y = self.size[1] / 2
      )
    )
