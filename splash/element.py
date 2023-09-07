'''
Base splash element
'''


import pygame as py

from core import sprites, screen


class Element(py.sprite.Sprite):
  '''A base class from which all splash sprites derive.
  
  This provides utility in show/hide functionality.
  '''

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

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
      sprites.active.add(self, layer = 0)
    else:
      sprites.active.remove(self)
