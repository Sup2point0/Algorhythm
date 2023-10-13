'''
Layered pygame sprite group
'''

import pygame as py


class LayeredGroup:
  '''A sprite group that stores its sprites in layers for ordered rendering.
  
  The layers are ordered with 0 at the top – when rendering, sprites in layer 0 will cover those in layer 1, and so on.
  '''

  def __init__(self, layers = 1):
    '''Create a group with a number of layers.'''

    self.groups = [py.sprite.Group() for i in range(layers)]

  def add(self, *sprites, layer: int = None):
    '''Add sprites to a layer of the group.
    
    If `layer` is not specified, a new layer will be created below the existing layers. If `layer` exceeds the current number of layers, new layers will be created to accomodate.
    '''

    if layer is None:
      layer = self.layers
    
    if layer >= self.layers:
      while layer >= self.layers:
        self.groups.append(py.sprite.Group())

    self.groups[layer].add(sprites)

  def remove(self, *sprites):
    '''Remove sprites from all layers of the group.'''

    for group in self.groups:
      group.remove(sprites)

  def empty(self):
    '''Remove all sprites from all layers of the group. Note that this does not delete the layers.'''

    for group in self.groups:
      group.empty()

  def insert(self, layer = None):
    '''Insert a new layer into the group.
    
    If `layer` is not specified, a new layer will be created below the existing layers.
    '''

    if layer is None:
      self.groups.append(py.sprite.Group())
    else:
      self.groups.insert(layer, py.sprite.Group())

  def reduce(self):
    '''Delete all empty layers.'''

    for group in self.groups:
      if not group.sprites:
        self.groups.remove(group)

  def draw(self, surface, flags = 0):
    '''Render the sprites in the group to a surface, in the order of their layers.'''

    for group in self.groups[::-1]:
      group.draw(surface, special_flags = flags)

  def __getitem__(self, index):
    return self.groups[index]

  def __len__(self):
    return sum(len(group) for group in self.groups)
  
  @ property
  def layers(self):
    '''The number of layers in the group.'''

    return len(self.groups)
