'''
Base splash element
'''

import pygame as py

from core import screen, sprites
from resource.sprite import Sprite


class Displayed:
  '''Settings for displaying a sprite.'''

  def __init__(self, *, show = None, hide = None, layer = None, fade = False, lock = None):
    '''Create a display settings configuration.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `show` | `set[str]` | Set of screen states to show the sprite. |
    | `hide` | `set[str]` | Set of screen states to hide the sprite. |
    | `false` | `bool` | Show or hide the sprite with a fade animation. |
    | `layer` | `int` | Layer to render sprite. |
    | `lock` | `Callable` | Function called to check if sprite should be locked from interaction. |
    '''

    if hide:
      self.show = set(state for state in screen.states if state not in hide)
    else:
      self.show = show or set()

    self.layer = layer or sprites.active.layer["splash"]
    self.fade = fade
    self.lock = lock or (lambda: False)


class Element(Sprite):
  '''Base class from which all splash sprites derive.'''

  class Style:
    '''Base style class from which all style classes derive.'''

    def update(self, **kwargs):
      '''Update style settings.

      Useful for dynamically altering a style setting.
      '''

      for kwarg in kwargs:
        if hasattr(self, kwarg):
          self.__setattr__(kwarg, kwargs[kwarg])
  

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
    | `interact` | `bool` | Whether element can be hovered or clicked. |
    | `display` | `splash.Displayed` | Sprite display settings. |

    Other base parameters are inherited from `resource.Sprite`.
    '''
    
    super().__init__(pos = pos, align = (0, 0), groups = groups)

    self.id = id
    self.display = display

    if interact:
      self.lock = display.lock
      self.hover = False
      self.click = False
    
    # add to relevant splash sprite groups
    for state in screen.states:
      if state.name in display.show:
        sprites.splash[state.name].add(self)

  def visible(self):
    '''Show or hide sprite depending on current screen state.'''

    if (
      screen.state.name in self.display.show or
      self.display.hide and screen.state.name not in self.display.hide
    ):
      sprites.active.add(self, layer = self.display.layer)
    else:
      sprites.active.remove(self)

  def interact(self, root = None) -> str:
    '''Detect hover and click interactions with element and return state as a string.

    If element is clicked, call `root` if passed in, or `self.root` if available.
    '''

    if self.lock():
      return "lock"

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
      
      return "idle"

    else:  # not hovering
      self.hover = False
      self.click = False
      return "idle"
