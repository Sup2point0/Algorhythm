'''
Implements the `Slider` and `Slide` classes for scrolling through pages and configuring settings.

A slider consists of the `Slider` and `Slide` classes, where the `Slide` implements the internal functionality of the slider, and the `Slider` is the sprite that is updated and rendered.

(This is a similar structure to `TabView`s and `Tab`s. It also leaves room open for adding multiple sliders, should that become needed or useful in the future.)
'''

import math

import pygame as pg

from core import screen, ui
from innate.sprite import Sprite

from splash.elements import Element
from splash.buttons import Button


class Slide(Element):
  '''The button-like element that controls a slider.'''

  class Style(Element.Style):
    '''A slide style.'''

    def __init__(self,
      shape,
      size,
      cols = None,
      length = None,
    ):
      '''Create a slide style.

      | parameter | type | notes |
      | :-------- | :--- | :---- |
      | `shape` | `str['circle', 'line']` | |
      | `size` | `num` | Radius or width of slider. |
      | `cols` | `dict[str, Color]` | Colours for different interaction states. |
      | `length` | `Callable -> num[0.0~1.0]` | Function called to calculate slide length (only for line). |
      '''

      self.shape = shape
      self.size = size
      self.length = (length or (
        lambda: screen.y / (screen.scroll[screen.state].upper + screen.y)
      )) # finds proportion of total space currently being viewed for page scrolling

      super()._config_cols_(cols, ui.col.slide)

  ###
  def __init__(self, root, style = None):
    '''Create a slide.

    | parameter | type | notes |
    | :-------- | :--- | :---- |
    | `root` | `innate.BoundValue` | Value which slide alters. |
    | `style` | `Slide.Style` | Style settings for slide. |
    '''

    super().__init__(id = None, interact = True, drag = True)

    self.root = root
    self.style = style or Slide.Style()

  def _align_(self) -> str:
    '''Utility function to find alignment of slide.'''
    return "top" if self.slider.dir else "left"

  def update(self):
    '''Process slide interaction and rendering.'''

    ## calculate size
    if self.style.shape == "line":
      self.size = (
        self.style.size or self.slider.width,
        self.slider.length * self.style.length()
      )
      print(f"slide.size = {self.size}")
      # flip dimensions for horizontal
      if self.slider.dir == 0:
        self.size = self.style.size[::-1]

    elif self.style.shape == "circle":
      self.size = (self.style.size * 2 or self.slider.width) * 2

    ## draw
    self.surf = pg.Surface(self.size, pg.SRCALPHA)
    self.rect = self.surf.get_rect()

    dist = self.root.upper - self.root()
    upper = self.slider.length * (1 - self.style.length())
    print(f"slide.dist = {dist}, slide.upper = {upper}")

    self.rect.__setattr__(self._align_(), dist / upper)

    ...  ## NOTE?

    interact = super().interact()
    self.col = self.style.cols[interact]

    if self.style.shape == "circle":
      pg.draw.circle(self.surf, self.col,
        center = self.size / 2,
        radius = self.style.size,
      )
    elif self.style.shape == "line":
      pg.draw.rect(self.surf, self.col, self.rect,
        border_radius = math.floor(self.style.size / 2)
      )


class Slider(Element):
  '''An interactive slider that can be freely dragged between 2 extreme values, or between several different notches on a scale.
  '''

  class Style(Element.Style):
    '''A slider style.'''

    def __init__(self,
      col = None,
      notch = None,
    ):
      '''Create a slider style.

      | parameter | type | notes |
      | :-------- | :--- | :---- |
      | `col` | `Color` | Colour of slider. Colour of slide is set in `Slide.Style`. |
      | `notch` | ? | Style of notches. |
      '''

      self.col = col or ui.col.slider
      self.notch = notch

  ###
  def __init__(self, id, pos,
    size,
    slide,
    values = (0.0, 1.0),
    style = None,
    display = None,
  ):
    '''Create a slider. A `Slide` must also be created and passed in, binding the 2 objects together.

    | parameter | type | notes |
    | :-------- | :--- | :---- |
    | `size` | `num, num` | Dimensions of slider. Direction is automatically determined by which is longer. |
    | `slide` | `Slider.Slide` | Slide to control slider. |
    | `values` | `Iterable[num]` / `innate.BoundValue` | Values of slider. |
    | `style` | `Slider.Style` | Style settings for slider. |

    Other base parameters are inherited from `splash.Element`.
    '''

    super().__init__(id, pos, interact = True, display = display)

    self.size = size
    self.length = max(self.size)
    self.width = min(self.size)
    self.dir = int(self.size[0] < self.size[1])
    '''Direction of slider. `0` = horizontal, `1` = vertical.'''

    self.style = style or Slider.Style()

    self.slide = slide
    slide.slider = self
    # tie both elements to each other

    if len(values) < 2:
      raise ValueError("Slider must have at least 2 values")
    self.values = values
    self.snap = (len(values) == 2)
    '''Whether slider snaps to notches or can be freely dragged.'''

  def update(self):
    self.slide.update()
    self.render()
    super().position()

  def render(self):
    '''Update surf and rect of the slider.'''

    self.surf = pg.Surface(self.size, pg.SRCALPHA)
    self.rect = self.surf.get_rect()

    pg.draw.rect(self.surf, self.style.col,
      rect = (0, 0, *self.size),
    )

    self.surf.blit(self.slide.surf, self.slide.rect)
