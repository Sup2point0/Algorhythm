'''
Implements the `Action` class for triggering level events and the specialised `Hint` class for tutorials.
'''

import pygame as py

from core import level, screen, sprites
from innate.sprite import Sprite
import util


class Action:
  '''An event that can be triggered within a level.'''

  def __init__(self, beat, action, loop = None):
    '''Create an action event.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `beat` | `num` | Beat on which event should occur. |
    | `action` | `Callable` | Function called when event occurs. |
    | `loop` | `int, num` | How many times to loop the event (default is 1), and the gap in beats between each repeat. |
    '''

    self.beat = beat
    self.activate = Action._handler_(action, loop)
    self.loop = loop or (1, 0)
    self.looped = 0

  def _handler_(action, loop):
    '''Internal function to wrap a provided action.'''

    def root(self):
      if level.beat > self.beat:
        action()
        
        self.looped += 1
        if self.looped >= self.loop[0]:
          self.kill()
        else:
          self.beat += self.loop[1]

    return root


class Hint(Sprite, Action):
  '''Text that displays during a level.'''

  class Highlight:
    '''A highlighted (non-darkened) part of the hint overlay.'''

    def __init__(self, pos, size):
      '''Create a rectangular highlighted area.

      | parameter | type | description |
      | :-------- | :--- | :---------- |
      | `pos` | `num, num` | Position of centre of rectangle. |
      | `size` | `num, num` | Dimensions of area. |
      '''

      self.pos = pos
      self.size = size

      self.rect = py.Rect(0, 0, 0, 0)

    def update(self):
      self.rect.width = util.slide(self.rect.width, self.size[0])
      self.rect.height = util.slide(self.rect.height, self.size[1])
      self.rect.centre = self.pos


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
    self.text = text
    self.highlights = highlights

    class anim:
      tick = 0
      alpha = util.Alpha(0, bounds = (0, 128))

    self.anim = anim

  def activate(self):
    if level.beat > self.beat:
      if not self.alive():
        sprites.active.add(self, layer = sprites.active.layer["hints"])

  def update(self):
    if self.anim.tick:
      self.anim.tick += 1
      if self.anim.tick > self.dur:  # fade out
        self.anim.alpha.alt(-4)
        if self.anim.alpha.bounds():
          self.kill()
    else:  # fade in
      self.anim.alpha.alt(4)
      if self.anim.alpha.bounds():
        self.anim.tick = 1

    self.surf = py.Surface(screen.size, py.SRCALPHA)
    self.surf.fill([255, 255, 255, self.anim.alpha()])
    self.rect = self.surf.get_rect()

    if self.highlights and self.anim.tick > 30:
      for each in self.highlights:
        each.update()
        self.surf.blit(py.Surface(each.anim.size, py.SRCALPHA), each.rect)

    if self.text:
      self.surf.blit(self.text, self.text.rect)
