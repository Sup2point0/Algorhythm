'''
Implements the `PopEffect` class for note hit visual effects.
'''

import pygame as pg

from core import sprites, config, opt
from innate import Alpha
from innate.sprite import Sprite
import util


class PopEffect(Sprite):
  '''An animated effect when a note is hit.'''

  def __init__(self, pos, prec = "hit", size = None, speed = None):
    '''Create a note hit effect.

    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `pos` | `num, num` | The position to create the effect. |
    | `prec` | `str` | The precision of the hit, which affects the colour. |
    | `size` | `num` | The greatest the radius of the circles involved in the effect will be. |
    | `speed` | `num` | How quickly the effect vanishes. |
    '''

    super().__init__(pos = pos, groups = [sprites.effects])
    super().show("effects")

    self.col = opt.col.perfect if prec == "perfect" else opt.col.hit
    self.size = size or config.effect.size * opt.effect.size()
    self.speed = speed or config.effect.speed * opt.effect.speed()

    class anim:
      tick = 0
      alpha = Alpha(192)
      pop = self.size
      poof = 1
      boop = 1

    self.anim = anim

  def update(self):
    self.anim.tick += 1

    ## animate
    self.anim.alpha.alt(-self.speed)
    if self.anim.alpha.bounded():
      return self.kill()

    self.anim.pop = util.slide(self.anim.pop, 1, speed = 2)
    self.anim.poof = util.slide(self.anim.poof, self.size, speed = 2)
    self.anim.boop = util.slide(self.anim.boop, self.anim.poof, speed = 2)

    print(f"pop = {self.anim.pop}, poof = {self.anim.poof}, boop = {self.anim.boop}")

    ## render
    self.surf = pg.Surface([self.size * 2] * 2, pg.SRCALPHA)
    self.rect = self.surf.get_rect()
    self.rect.center = self.pos
    # pg.draw.circle(
    #   surface = self.surf,
    #   color = self.col[:3] + [self.anim.alpha.value],
    #   center = [self.size] * 2,
    #   radius = self.anim.pop,
    #   width = 0,
    # )
    pg.draw.circle(
      surface = self.surf,
      color = self.col[:3] + [self.anim.alpha.value],
      center = [self.size] * 2,
      radius = self.anim.poof,
      width = round(self.anim.poof - self.anim.boop),
    )
