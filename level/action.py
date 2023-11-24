'''
Implements the `Action` class for triggering level events and the specialised `Hint` class for tutorials.
'''

import pygame as py

from core import level, screen, sprites, config
from innate.sprite import Sprite
import util


class Action:
  '''An event that can be triggered within a level.'''

  def __init__(self, beat, action, loops = False, interval = None):
    '''Create an action event.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `beat` | `num` | Beat on which event should occur. |
    | `action` | `Callable` | Function called when event occurs. |
    | `loop` | `bool` | Whether action loops. |
    | `interval` | `num` | Beat interval between each loop. |
    '''

    self.beat = beat
    self.action = self._handler_(action)

    self.loops = loops
    if loops:
      self.actions = [Action(beat + i * interval, action) for i in range(loops)]

  def _handler_(self, action):
    '''Internal function to wrap a provided action.'''

    def root():
      if level.beat > self.beat:
        action()
        self.kill()

    return root


class Hint(Sprite, Action):
  '''Text that displays during a level.'''

  class Highlight:
    '''A highlighted (non-darkened) part of the hint overlay.'''

    def __init__(self, *highlight):
      '''Create a rectangular highlighted area.

      | parameter | type | description |
      | :-------- | :--- | :---------- |
      | `x`, `y` | `num, num` | Position of centre of rectangle. |
      | `width`, `height` | `num, num` | Dimensions of area. |
      '''

      rect = py.Rect(*highlight)
      self.pos = (rect.x, rect.y)
      self.size = rect.size

      self.rect = py.Rect(0, 0, 0, 0)

    def update(self):
      self.rect.width = util.slide(self.rect.width, self.size[0], speed = 10)
      self.rect.height = util.slide(self.rect.height, self.size[1], speed = 10)
      self.rect.center = self.pos
      self.surf = py.Surface(self.rect.size, py.SRCALPHA)
      self.surf.fill([0, 0, 0, 0])


  def __init__(self, beat, dur, text = None, highlights = None):
    '''Create a level hint.

    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `beat` | `num` | Beat on which to trigger hint. |
    | `dur` | `int` | Duration (in ticks) to display hint. |
    | `text` | `splash.Text` | Text element to render on darkened overlay. |
    | `highlights` | `list[Hint.Highlight]` | Part(s) of screen to highlight. |

    Although this class does not utilise any functionality from `Action`, it needs to inherit from it to be detected and activated when the chart is processed.
    '''

    super().__init__()

    self.beat = beat
    self.dur = dur
    self.loops = False
    self.text = text
    self.highlights = highlights

    class anim:
      tick = 0
      alpha = util.Alpha(0, bounds = (0, 128))

    self.anim = anim

  def activate(self):
    if not self.alive():
      sprites.actions.add(self)
      sprites.active.add(self, layer = sprites.active.layer["hints"])

  def update(self):
    if self.anim.tick:
      if level.beat - self.anim.tick > self.dur:  # fade out
        self.anim.alpha.alt(-config.rate.fade / 2)
        if self.anim.alpha.bounded():
          self.kill()
    else:  # fade in
      self.anim.alpha.alt(config.rate.fade / 2)
      if self.anim.alpha.bounded():
        self.anim.tick = level.beat

    self.surf = py.Surface(screen.size, py.SRCALPHA)
    self.surf.fill([0, 0, 0, self.anim.alpha()])
    self.rect = self.surf.get_rect()

    if self.highlights:
      if level.beat - self.anim.tick > 1:
        for each in self.highlights:
          each.update()
          self.surf.blit(each.surf, each.rect)

    if self.text:
      self.text.surf.set_alpha(255 * self.anim.alpha() / self.anim.alpha.upper)
      self.surf.blit(self.text.surf, self.text.rect)
