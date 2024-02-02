'''
Implements the `Slider` and `Slide` classes for scrolling through pages and configuring settings.

A slider consists of the `Slider` and `Slide` classes, where the `Slide` implements the internal functionality of the slider, and the `Slider` is the sprite that is updated and rendered.

(This is a similar structure to `TabView`s and `Tab`s. It also leaves room open for adding multiple sliders, should that become needed or useful in the future.)
'''

import pygame as pg

from core import screen, ui
import innate

from splash.elements import Element
from splash.buttons import Button


class Slide(innate.Sprite):
  '''The button-like element that controls a slider.'''

  class Style(Element.Style):
    '''A slide style.'''

    def __init__(self,
      shape = None,
      size = None,
      cols = None,
      length = None,
    ):
      '''Create a slide style.

      | parameter | type | notes |
      | :-------- | :--- | :---- |
      | `shape` | `str`, `None` | `'circle'`, `'line'`
      | `size` | `num` | Radius or width of slider. |
      | `cols` | `dict[str, Color]` | Colours for different interaction states. |
      | `length` | `Callable -> num[0.0~1.0]` | Function called to calculate slide length (only for line). |
      '''

      super().__init__(
        shape = shape,
        size = size,
        length = length or (lambda: screen.y / screen.scoll[screen.state].upper),
        # finds proportion of total space currently being viewed for page scrolling
      )

      super()._config_cols_(cols, ui.col.slide)

  ###
  def __init__(self, root, style = None):
    '''Create a slide.

    | parameter | type | notes |
    | :-------- | :--- | :---- |
    | `root` | `innate.Value` | Value which slide alters. |
    | `style` | `Slide.Style` | Style settings for slide. |
    '''

    self.root = root
    self.style = style or Slide.Style()

  def _align_(self):
    '''Utility function to find alignment of slide as a `str`.'''
    return "top" if self.slider.dir else "left"

  def update(self):
    '''Process slide interaction and rendering.'''

    ## calculate size
    if self.style.shape == "line":
      self.size = (
        self.slider.width,
        self.slider.height * self.style.height()
      )
      if self.slider.dir == 0:  # flip dimensions for horizontal
        self.size = self.size[::-1]

    ## draw
    self.surf = pg.Surface(self.size, pg.SRCALPHA)
    self.rect = self.surf.get_rect()
    dist = self.root.upper - self.root()
    upper = self.slider.height * (1 - self.style.height())

    self.rect.__setattr__(self._align_(), dist / upper)

    ...

    interact = super().interact()
    self.col = self.style.cols[interact]

    if interact == "click":
      self.pos[...] = pg.mouse.get_pos()[1]
        # util.restrict(self.rect.top, lower = self.  ## FIXME

    if self.style.shape == "circle":
      pg.draw.circle(self.surf, self.col, radius = self.size)  # FIXME
    elif self.style.shape == "line":
      pg.draw.rect(self.surf, self.col, ...)  # FIXME


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
      '''

      super().__init__(
        col = col or ui.slider.col,
        notch = notch,
      )

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
    | `style` | `Slider.Style` | Style settings for slider. |
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
    self.free = (len(values) == 2)
    '''Whether slider can be freely dragged, or snaps to notches.'''

    self.slide.render()
    self.render()
    super().position()

  def update(self):
    self.slide.update()
    self.render()

  def render(self):
    '''Update surf and rect of the slider.'''

    self.surf = pg.Surface(self.size, pg.SRCALPHA)
    self.rect = self.surf.get_rect()

    pg.draw.rect(self.surf,
      color = self.col,
    )

    self.surf.blit(self.slide.surf, self.slide.rect)
