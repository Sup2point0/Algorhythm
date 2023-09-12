'''
Animation effects
'''

import pygame as py

from core import sprites, ui, opt
import util


class PopEffect(py.sprite.Sprite):
  '''A class to contain the component sprites that make up the animated effect when a note is hit.'''

  def __init__(self, pos, acc = "hit", size = None, speed = None):
    '''Create a note hit effect.

    | argument | type | description |
    | :------- | :--- | :---------- |
    | `pos` | `(num, num)` | The position to create the effect. |
    | `acc` | `str` | The accuracy of the hit, which affects effect appearance. |
    | `size` | `num` | The greatest the radius of the circles involved in the effect will be. |
    | `speed` | `(int, num)` | How quickly the effect vanishes. The first value represents how many frames will pass before it starts fading, the second how much transparency will increase per frame. |
    '''

    super().__init__(sprites.effects)
    sprites.active.add(self, layer = 2)  # NOTE?

    self.pos = pos
    self.col = ui.col.perfect if acc == "perfect" else ui.col.hit
    self.size = size or ui.effect.popsize
    self.speed = speed or opt.effect.speed

    class anim:
      tick = 0
      alpha = util.Alpha(192)
      pop = self.size
      poof = 1
      boop = 1

    self.anim = anim

  def update(self):
    self.anim.tick += 1

    ## animate
    if self.anim.tick > opt.effect.speed[0]:
      self.anim.alpha.alt(-opt.effect.speed[1])
    if self.alpha.value == 0:
      return self.kill()

    self.anim.pop = util.slide(self.anim.pop, 1, 2)
    self.anim.poof = util.slide(self.anim.poof, self.size, 2)
    self.anim.boop = util.slide(self.anim.boop, self.anim.poof, 2)

    ## render
    self.image = py.Surface([self.size] * 2, py.SRCALPHA)
    self.rect = self.image.get_rect()
    self.rect.topleft = self.pos
    py.draw.circle(
      surface = self.image,
      radius = self.anim.pop
      ...,
      width = 0,
    )
    py.draw.circle(
      surface = self.image,
      radius = self.anim.poof,
      ...,
      width = self.anim.poof - self.anim.boop,
    )
