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

  def __init__(self, id: str, pos = None, display = None, groups = None):
    '''
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `id` | `str` | Unique ID to identify element. |
    | `pos` | `[num, num]` | Coordinates to position element. |
    | `display` | `splash.Displayed` | Sprite display settings. |
    | `groups` | `list[py.sprite.Group]` | Groups to add element to. |
    '''
    
    super().__init__(*groups)

    self.id = id
    self.display = display

    xy = pos or [0, 0]
    self.x = xy[0]
    self.y = xy[1]

  def visible(self):
    '''Show or hide sprite depending on current screen state.'''

    if (screen.state in self.display.show) and (screen.state not in self.display.hide):
      sprites.active.add(self, layer = self.display.layer)
    else:
      sprites.active.remove(self)

  @ property
  def pos(self):
    '''Coordinates of the element.'''

    return [self.x, self.y]
