'''
Base splash element
'''

import pygame as py

from core import sprites, screen


class Element(py.sprite.Sprite):
  '''Base class from which all splash sprites derive.'''

  def __init__(self,
    id: str,
    pos = None,
    layer = 1,
    display: list = None,
    fade: bool = False,
    groups: list = None
  ):
    '''
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `id` | `str` | Unique ID to identify element. |
    | `pos` | `[num, num]` | Coordinates to position element. |
    | `layer` | `int` | Which layer to render element. |
    | `display` | `list[str]` | List of screen states where element should be displayed. |
    | `fade` | `bool` | Shows or hides element with a fade animation. |
    | `groups` | `list[py.sprite.Group]` | Groups to add element to. |
    '''
    
    super().__init__(*groups)

    self.id = id
    self.slayer = layer
    self.display = display or []

    xy = pos or [0, 0]
    self.x = xy[0]
    self.y = xy[1]

    fades = fade

    class anim:
      fade = fades

    self.anim = anim

  def visible(self):
    '''Show or hide sprite depending on current screen state.'''

    if isinstance(self.display, dict):
      visible = (
        screen.state not in self.display or
        screen.state in self.display and self.display[screen.state]
      )
    else:
      visible = (screen.state in self.display)

    # TODO use self.layer
    if visible:
      sprites.active.add(self, layer = self.slayer)
    else:
      sprites.active.remove(self)

  @ property
  def pos(self):
    '''X and Y position of the element.'''

    return [self.x, self.y]
