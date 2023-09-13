'''
Reusable sprite functionality

Often, sprites will take a `root` argument when instantiated. This is a `Callable` (a function) that will be called to provide the sprite with functionality. For instance, a button would call its `root` when clicked.

This file centralises the functionality of various sprites, as well as providing functions to dynamically generate other functions. This is useful for sprites that have similar but slightly differing functionality – such as a button switching to a particular screen.
'''

import random as ran

from core import game, sprites, screen, config
import util

from levels import levels


class switch:
  '''Functions involving changing the screen state.'''

  def state(state: str):
    '''Change screen state to `state`.'''

    def root():
      screen.switch = state
      screen.fade = "out"

    return root

  def back():
    '''Go back to the previous screen.'''

    switch.state(screen.track[-2])()

  def tutorial():
    '''Play the tutorial.'''

    switch.state("play")()
    levels.charts[0].start(difficulty = 0)


class shock:
  '''Functions for shock notes. The shock note calling the root should pass itself in as an argument.'''
  
  def key(key: str | list[str] = None):
    '''Change key of lane.'''
    
    def root(self):
      if not isinstance(key, str):
        key = util.randkey(key)
      
      self.lane.key = key
    
    return root
  
  def lane(index = None):
    '''Change index of lane.'''
    
    def root(self):
      self.lane.switch(index)
    
    return root
  
  def lanes(lanes: list[int] = None):
    '''Shuffle all lanes around.'''
    
    def root(self):
      if lanes is None:
        lanes = list(range(len(sprites.lanes)))
      
      pend = [lane for lane in sprites.lanes if lane.index in lanes]
      ran.shuffle(pend)
      
      for i, lane in enumerate(pend):
        lane.index = lanes[i]
    
    return root


class fade:
  '''Functions for screen covers.'''

  def total(self):
    match screen.fade:
      case "out":
        self.alpha += config.faderate
        if self.alpha == 255:
          screen.fade = "dark"
      case "in":
        self.alpha -= config.faderate
        if self.alpha == 0:
          screen.fade = None
      case None:
        self.alpha = 0

  def partial(self):
    if not game.state:
      self.alpha += config.faderate
    else:
      self.alpha -= config.faderate
