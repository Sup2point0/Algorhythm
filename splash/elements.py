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
    | `hide` | `set[str]` | Set of screen states to hide the sprite. |
    | `layer` | `int` | Layer to render sprite. |
    | `fade` | `bool` | Show or hide the sprite with a fade animation. |
    | `root` | `Callable -> bool` | Function called to check if sprite should be rendered. |
    | `lock` | `Callable -> bool` | Function called to check if sprite should be locked from interaction. |
    '''

    if hide:
      self.show = set(state for state in screen.states if state not in hide)
    else:
      self.show = show or set()

    self.layer = layer or sprites.active.layer["splash"]
    self.fade = fade
    self.root = root or (lambda: True)
    self.lock = lock or (lambda: False)


class Element(Sprite):
  '''Base class from which all splash sprites derive.'''

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
    | `interact` | `bool` | Whether element can be hovered or clicked. |
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
    
    # add to relevant splash sprite groups
    for state in screen.states:
      if state.name in display.show:
        sprites.splash[state.name].add(self)

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
