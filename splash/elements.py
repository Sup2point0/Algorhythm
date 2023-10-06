'''
Base splash element
'''

import pygame as py

from core import screen, sprites
from resource.sprite import Sprite


class Displayed:
  '''Settings for displaying a sprite.'''

  def __init__(self, *,
    show = None,
    hide = None,
    layer = None,
    fade = False,
    root = None,
    lock = None,
  ):
    '''Create a display settings configuration.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `show` | `set[str]` | Set of screen states to show the sprite. |
    | `hide` | `set[str]` | Set of screen states to hide the sprite. If specified, the sprite will default to being shown in every screen state. |
    | `layer` | `int` | Layer to render sprite. |
    | `fade` | `bool` | Show or hide the sprite with a fade animation. |
    | `root` | `Callable -> bool` | Function called to check if sprite should be rendered. |
    | `lock` | `Callable -> bool` | Function called to check if sprite should be locked from interaction. |
    '''

    if hide:
      self.show = screen.states - hide
    else:
      self.show = show or set()

    self.layer = layer or sprites.active.layer["splash"]
    self.fade = fade
    self.root = root or (lambda: True)
    self.lock = lock or (lambda: False)


class Element(Sprite):
  '''Base class from which all splash sprites derive.'''
  
  class Style:
    '''Base class from which all style classes derive.'''

    def update(self, **kwargs):
      '''Update style settings using keyword arguments.'''

      for kwarg in kwargs:
        if hasattr(self, kwarg):
          self.__setattr__(kwarg, kwargs[kwarg])

  
  def __init__(self,
    id: str,
    pos = None,
    interact = False,
    display = None,
  ):
    '''
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `id` | `str` | Unique ID to identify element. |
    | `interact` | `bool` | Whether element can be hovered over or clicked on. |
    | `display` | `splash.Displayed` | Sprite display settings. |

    Other base parameters are inherited from `resource.Sprite`. `groups` is not inherited, since all splash sprites are automatically added to the suitable `sprites.splash` group.
    '''
    
    super().__init__(pos = pos, align = (0, 0))

    self.id = id
    self.display = display

    if interact:
      self.locked = display.lock
      self.hover = False
      self.click = False
    
    for state in display.show:
      sprites.splash[state].add(self)

  # def visible(self):
  #   '''Show or hide sprite depending on current screen state.'''

  #   if (
  #     screen.state.name in self.display.show or
  #     self.display.hide and screen.state.name not in self.display.hide
  #   ):
  #     sprites.active.add(self, layer = self.display.layer)
  #   else:
  #     sprites.active.remove(self)

  def interact(self, root = None) -> str:
    '''Detect hover and click interactions with element and return state as an uppercase string.

    If element is clicked, call `root` if passed in, or `self.root` if available.
    '''

    if self.lock():
      return "LOCK"

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
        return "HOVER"

      elif down and self.hover:  # clicked
        self.click = True
        return "CLICK"
      
      return "IDLE"

    else:  # not hovering
      self.hover = False
      self.click = False
      return "IDLE"
