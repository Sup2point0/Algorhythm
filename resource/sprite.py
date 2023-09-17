'''
Base sprite functionality
'''

import pygame as py


class Sprite(py.sprite.Sprite):
  '''Base class from which all game sprites derive, providing inherent attributes and utility.'''

  def __init__(self,
    pos = None,
    align = (0, 0),
    groups = None,
  ):
    '''
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `id` | `num, num` | Position coordinates. |
    | `align` | `int, int` | Alignment of sprite. 
    '''

    ...
