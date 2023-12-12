'''
Implements root functions for reusable sprite functionality.

Often, sprites will take a `root` argument when instantiated. This is a `Callable` (a function) that will be called to provide the sprite with functionality. For instance, a button would call its `root` when clicked.

This module centralises the functionality of various sprites, as well as providing functions to dynamically generate other functions. This is useful for sprites that have similar but slightly differing functionality – such as a button switching to a particular screen.
'''

import random

import pygame as pg

from core import game, screen, sprites, config
import util

from levels import levels


class switch:
  '''Functions involving changing the screen state.'''

  def state(state: str):
    '''Change screen state to `state`.'''

    def root():
      screen.switch = state

    return root

  def back():
    '''Go back to the previous screen.'''

    screen.switch = screen.track[-2]

  def tutorial():
    '''Play the tutorial.'''

    levels.charts["tutorials"][0].start(difficulty = 0)
    switch.state("play")()


def select(var, state):  # TODO add class hierarchy?
  '''Change `var` in `game.select` to `state`.'''

  def root():
    game.select[var] = state

  return root

def scroll(state):
  return (lambda: screen.scroll[state]())


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
      random.shuffle(pend)
      
      for i, lane in enumerate(pend):
        lane.index = lanes[i]
    
    return root


class fade:
  '''Functions for screen covers.'''

  def total(self):
    match screen.fade:
      case "out":
        self.alpha.alt(config.rate.fade)
        if self.alpha.bounded():
          screen.fade = "dark"
      case "in":
        self.alpha.alt(-config.rate.fade)
        if self.alpha.bounded():
          screen.fade = None
      case None:
        self.alpha.set(0)

  def partial(self):
    self.alpha.alt(config.rate.fade * (-1 if game.state else 1))