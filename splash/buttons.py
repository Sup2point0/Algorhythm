'''
Buttons
'''

import pygame as py

from core import sprites, ui
import util

from splash.elements import Element
from splash.text import Text


class Button(Element):
  '''A clickable button that invokes an action.'''

  class Style(Element.Style):
    '''A button style.'''
  
    def __init__(self, *, edge = "round", col: dict = None, textstyle = None):
      '''Create a button style.
      
      | parameter | type | description |
      | :-------- | :--- | :---------- |
      | `edge` | `str` | Edge style – can be `round`, `sharp` or `angular`. |
      | `col` | `dict` | The colours for the different states of the button. |
      | `textstyle` | `Text.Style` | Style settings for text on button. |
      '''
  
      self.edge = edge
  
      cols = col or {}
      self.cols = {
        state: cols.get(state, vars(ui.col.button)[state])
        for state in ["idle", "hover", "click", "lock"]
      }
      self.col = self.cols["idle"]
      self.text = textstyle or Text.Style()

  
  def __init__(self, id, pos, size, text, root, style = None, display = None):
    '''Create a clickable button.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `size` | `[int, int]` | Dimensions of button. |
    | `text` | `str` | Text to display on button. |
    | `root` | `Callable` | Function called when button is clicked. |
    | `style` | `Button.Style` | Style settings for button. |

    Other base parameters are inherited from `splash.Element`.
    '''

    super().__init__(id, pos, interact = True, display = display, groups = [sprites.splash])

    self.size = size
    self.text = text
    self.root = root
    self.style = style or Button.Style()

    class anim:
      col = self.style.col
      coltick = 0

    self.anim = anim

  def update(self):
    super().visible()
    
    ## process
    self.image = py.Surface(self.size, py.SRCALPHA)
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = util.root(self.rect, *self.pos)
    
    interaction = super().interact()
    self.style.text.update(col = self.style.text.cols[interaction])
    if interaction in {"idle", "hover"}:  # NOTE is set faster?
      if interaction == "idle":
        if self.anim.coltick > 0:
          self.anim.coltick -= 0.1
      else:
        if self.anim.coltick < 1:
          self.anim.coltick += 0.1
      
      self.anim.col = util.interpolate.col(
        start = self.style.cols["idle"],
        stop = self.style.cols["hover"],
        percent = self.anim.coltick,
      )
      self.anim.col = self.style.cols[interaction]
    
    else:
      self.anim.col = self.style.cols[interaction]
    
    ## render
    py.draw.rect(
      surface = self.image,
      color = py.Color(self.anim.col),
      rect = py.Rect(0, 0, *self.size),
      width = 0,
      border_radius = min(self.size) // 3,  # FIXME value
    )
    
    rendered = Text.render(self.text, self.style.text)
    self.image.blit(
      source = rendered[0],
      dest = util.root(
        rect = rendered[1],
        x = self.size[0] / 2,
        y = self.size[1] / 2
      )
    )
