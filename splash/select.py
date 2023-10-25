'''
Implements the `SeriesSelect` and `TrackSelect` classes for selecting series or tracks.
'''

import pygame as py

from core import screen, sprites, ui, opt
from innate import Object
import util

from splash import roots
from splash.elements import Element, Displayed
from splash.text import Text
from splash.buttons import Button

from levels import levels


class SeriesSelect(Element):
  '''Represents a stylised button for selecting a series in the series selection menu.'''

  def __init__(self, id,
    series,
    cover = None,
    lock = None,
    locktext = None,
  ):
    '''Create a button for selecting a series.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `series` | `str` | Series selected when button is clicked. |
    | `cover` | `str` | File name from which to load image asset for button background. |
    | `lock` | `Callable -> bool` | Function called to check if series is locked. |
    | `locktext` | `str` | Text displayed if series is locked. |

    Other base parameters are inherited from `splash.Element`.
    '''

    super().__init__(id, anim = True, interact = True,
      display = Displayed(
        show = {"select"},
        align = (0, -1),
        scroll = (lambda: screen.scroll["select"]()),
        layer = sprites.active.layer["splash"],
        lock = lock,
      ),
    )

    super(self, Object).__init__(
      size = ui.size.select.series,
      series = series,
      cover = util.asset(f"covers/{cover or 'none.png'}"),
      locktext = locktext,
      root = roots.switch.state(f"select.{series.lower()}"),
      style = Element.Style(
        cols = {
          "idle": ui.col.text,
          "hover": opt.col.accent,
          "click": opt.col.flavour,
        },
        blur = {
          "idle": 15,
          "hover": 5,
          "click": 5,
        },
      ),
    )

    self.anim.col = ui.col.text
    self.anim.blur = 20

  def update(self):
    self.surf = py.Surface(self.size, py.SRCALPHA)
    self.rect = self.surf.get_rect()
    self.position()
    super().position()

    if self.display.lock():
      self.lock()
    else:
      self.render()

  def position(self):
    self.x = util.cord(x = 0)[0]
    self.y = (100 +
      (ui.size.select.series + 50)
    * levels.charts.index(self.series)
    )

  def render(self):
    interact = super().interact()
    self.anim.col = self.style.cols[interact]
    self.anim.blur = self.style.blur[interact]

    rendered = Text.render(self.series,
      style = Text.Style(size = 20, col = self.anim.col)
    )
    self.surf.blit(rendered[0],
      dest = util.root(rendered[1], self.size[0] / 2, self.size[1] / 2)
    )

  def lock(self):
    # TODO render dark rectangle

    if self.locktext:
      rendered = Text.render(self.locktext,
        style = Text.Style(size = 16)
      )
      self.surf.blit(rendered[0],
        dest = util.root(rendered[1], self.size[0] / 2, self.size[1] / 2)
      )


class TrackSelect(SeriesSelect):
  '''Represents a stylised button for selecting a track in the track selection menu.'''

  def __init__(self, id,
    series,
    track,
    cover = None,
    lock = None,
    locktext = None,
  ):
    '''Create a button for selecting a track.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `series` | `str` | In-game series which the track belongs to. |
    | `track` | `level.Track` | Track selected when button is clicked. |
    | `lock` | `Callable -> bool` | Function called to check if track is locked. |
    | `locktext` | `str` | Text displayed if track is locked. |

    Other base parameters are inherited from `splash.Selector` and `splash.Element`.
    '''

    display = f"select.{series.lower()}"

    super().__init__(id, anim = True, interact = True,
      display = Displayed(
        show = display,
        align = (0, -1),
        scroll = (lambda: screen.scroll[display]()),
        layer = sprites.active.layer["splash"],
        lock = lock,
      ),
    )

    super(self, Object).__init__(
      track = track,
      size = ui.size.select.track,
      cover = util.asset(f"covers/{cover or 'none.png'}"),
      locktext = locktext,
      root = roots.select("track", track),
      style = Element.Style(
        cols = {
          "idle": ui.col.text,
          "hover": opt.col.accent,
          "click": opt.col.flavour,
        },
        blur = {
          "idle": 15,
          "hover": 5,
          "click": 5,
        },
      ),
    )

  def position(self):
    self.x = util.cord(x = -0.5)[0]
    self.y = (100 +
      (ui.size.select.track + 50)
    * sprites.splash["select.tracks"].index(self.id)
    )

  def render(self):    
    # TODO blur image
    ...

    rendered = Text.render(self.track.name,
      style = Text.Style(size = 20, col = self.anim.col)
    )
    self.surf.blit(rendered[0],
      dest = util.root(rendered[1], 25, self.size[1] - 25, align = (-1, 1))
    )

    if not self.track.artist:
      return

    rendered = Text.render(self.track.artist,
      style = Text.Style(size = 16, col = self.anim.col)
    )
    self.surf.blit(rendered[0],
      dest = util.root(rendered[1], 25, 25, align = (-1, -1))
    )
