'''
Level events
'''

import pygame as py

from core import sprites
import util


class Action:
  '''An event that can be triggered within a level.'''

  def __init__(self, beat, action, loop = None):
    '''Create an action event.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `beat` | `num` | Beat on which event should occur. |
    | `action` | `Callable` | Function called when event occurs. |
    | `loop` | `int, num` | How many times to loop the action, and the gap in beats between each repeat. |
    '''

    self.beat = beat
    self.activate = handler(action, loop)
    self.loop = loop
    self.looped = 0

  def handler(action, loop):  # TODO
    def root():
      if level.beat > self.beat:
        action()

    return root


class Hint(Action):
  '''Text that displays during a level.'''

  class Highlight:
    '''A highlighted (non-darkened) part of the hint overlay.'''

    def __init__(self, pos, size):
      '''Create a rectangular highlighted area.

      | parameter | type | description |
      | :-------- | :--- | :---------- |
      | `pos` | `num, num` | Position of the rectangle (centre). |
      | `size` | `num, num` | Dimensions of area. |
      '''

      self.pos = pos
      self.size = size

      self.rect = py.Rect(0, 0, 0, 0)  # NOTE remove if defaults to 0?

    def update(self):
      self.rect.width = util.slide(self.rect.width, self.size[0])
      self.rect.height = util.slide(self.rect.height, self.size[1])
      self.rect.centre = self.pos


  def __init__(self, dur, text = None, highlights: list[Highlight] = None):
    '''Create a level hint.

    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `dur` | `int` | Duration (in ticks) to display hint. |
    | `text` | `splash.Text` | Text element to render on darkened overlay. |
    | `highlights` | `list[Hint.Highlight]` | Part of screen to highlight. |
    '''

    self.dur = dur
    self.text = text
    self.highlights = highlights

    class anim:
      tick = 0
      alpha = util.Alpha(0, bounds = (0, 128))

    self.anim = anim

  def activate(self):
    sprites.actions.add(self)
    sprites.active.add(self, layer = sprites.layer["hints"])

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
    self.surf.fill(0xffffff)
    self.rect = self.surf.get_rect()

    if self.highlights and self.anim.tick > 30:
      for each in highlight:
        each.update()
        self.surf.blit(
          source = py.Surface(each.anim.size, py.SRCALPHA),
          dest = each.rect
        )

    if self.text:
      self.surf.blit(self.text, self.text.rect)

    self.surf.set_alpha(self.anim.alpha.value)

  @ property
  def image(self):
    return self.surf
