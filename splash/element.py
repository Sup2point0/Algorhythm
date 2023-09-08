'''
Base splash element
'''


import pygame as py

from core import sprites, screen


class Element(py.sprite.Sprite):
  '''A base class from which all splash sprites derive.
  
  This provides utility in show/hide functionality.
  '''

  def __init__(self, id, pos = None, layer = 1, display = None, fade = False, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.id = id
    self.layer = layer
    self.display = display or []

    xy = pos or [0, 0]
    self.x = xy[0]
    self.y = xy[1]

    class anim:
      fade = fade

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
      sprites.active.add(self, layer = self.layer)
    else:
      sprites.active.remove(self)

  @ property
  def pos(self):
    '''X and Y position of the element.'''

    return [self.x, self.y]
