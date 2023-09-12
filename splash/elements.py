'''
Base splash element
'''

import pygame as py

from core import sprites, screen


class Displayed:
  '''Settings for displaying a sprite.'''

  def __init__(self, *, show = None, hide = None, layer = None, fade = False):
    '''Create a display settings configuration.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `show` | `set[str]` | Set of screen states to show the sprite. |
    | `hide` | `set[str]` | Set of screen states to hide the sprite. |
    | `false` | `bool` | Show or hide the sprite with a fade animation. |
    | `layer` | `int` | Layer to render sprite. |
    '''

    self.show = show or set()
    self.hide = hide or set()
    self.layer = layer
    self.fade = fade


class Element(py.sprite.Sprite):
  '''Base class from which all splash sprites derive.'''

  def __init__(self,
    id: str,
    pos = None,
    interact = False,
    display = None,
    groups = None,
  ):
    '''
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `id` | `str` | Unique ID to identify element. |
    | `pos` | `[num, num]` | Coordinates to position element. |
    | `interact` | `bool` | Whether element can be hovered or clicked. |
    | `display` | `splash.Displayed` | Sprite display settings. |
    | `groups` | `list[py.sprite.Group]` | Groups to add element to. |
    '''
    
    super().__init__(*groups)

    self.id = id
    self.display = display

    xy = pos or [0, 0]
    self.x = xy[0]
    self.y = xy[1]

    if interact:
      self.hover = False
      self.click = False

  def visible(self):
    '''Show or hide sprite depending on current screen state.'''

    if (screen.state in self.display.show) and (screen.state not in self.display.hide):
      sprites.active.add(self, layer = self.display.layer)
    else:
      sprites.active.remove(self)

  def interact(self, root = None) -> str:
    '''Detect hover and click interactions with element and return state as a string.

    If element is clicked, call `root` if passed in, or `self.root` if available.
    '''

    down = py.mouse.get_pressed()[0]

    if self.rect.collidepoint(py.mouse.get_pos()):
      if not down:  # hovered
        if self.click:  # clicked and released
          if root:
            root()
          elif hasattr(self, "root"):
            self.root()
        self.hover = True
        self.click = False
        return "hover"

      elif down and self.hover:  # clicked
        self.click = True
        return "click"

    else:  # not hovering
      self.hover = False
      self.click = False
      return "idle"

  @ property
  def pos(self):
    '''Coordinates of the element.'''

    return [self.x, self.y]
