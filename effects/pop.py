'''
Note hit effects
'''

import pygame as py

from core import sprites, ui, opt
from resource.sprite import Sprite
import util


class PopEffect(Sprite):
  '''A class to contain the component sprites that make up the animated effect when a note is hit.'''

  def __init__(self, pos, acc = "hit", size = None, speed = None):
    '''Create a note hit effect.

    | argument | type | description |
    | :------- | :--- | :---------- |
    | `pos` | `num, num` | The position to create the effect. |
    | `acc` | `str` | The accuracy of the hit, which affects effect appearance. |
    | `size` | `num` | The greatest the radius of the circles involved in the effect will be. |
    | `speed` | `int, num` | How quickly the effect vanishes. The first value represents how many frames will pass before it starts fading, the second how much transparency will increase per frame. |
    '''

    super().__init__(pos = pos, groups = [sprites.effects])

    sprites.active.add(self, layer = sprites.active.layer["effects"])

    self.col = opt.col.perfect if acc == "perfect" else opt.col.hit
    self.size = size or opt.effect.size
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
    if self.anim.alpha.value == 0:
      return self.kill()

    self.anim.pop = util.slide(self.anim.pop, 1, speed = 2)
    self.anim.poof = util.slide(self.anim.poof, self.size, speed = 2)
    self.anim.boop = util.slide(self.anim.boop, self.anim.poof, speed = 2)

    ## render
    self.surf = py.Surface([self.size * 2] * 2, py.SRCALPHA)
    self.rect = self.surf.get_rect()
    self.rect.center = self.pos
    py.draw.circle(
      surface = self.surf,
      color = self.col[:3] + [self.anim.alpha.value],
      center = [self.size] * 2,
      radius = self.anim.pop,
      width = 0,
    )
    py.draw.circle(
      surface = self.surf,
      color = self.col[:3] + [self.anim.alpha.value],
      center = [self.size] * 2,
      radius = self.anim.poof,
      width = round(self.anim.poof - self.anim.boop),
    )
