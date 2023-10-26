'''
Implements the `SeriesSelect` and `TrackSelect` classes for selecting series or tracks.
'''

import pygame as py

from core import screen, sprites, ui, config, opt
from innate import Object
import util

from splash import roots
from splash.elements import Element, Displayed
from splash.text import Text

from levels import levels

import effects.blur


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

    class root:
      surf = util.find.asset(f"covers/{cover or 'none.png'}")
      width, height = surf.get_size()

    width, height = ui.size.select.series
    if root.width / root.height < width / height:
      scale = width / root.width
    else:
      scale = height / root.height

    Object.__init__(self,
      size = (width, height),
      series = series,
      cover = py.transform.scale_by(root.surf, scale),
      locktext = locktext,
      root = roots.switch.state(f"select.{series.lower()}"),
      style = Element.Style(
        cols = {
          "idle": ui.col.text.idle,
          "hover": opt.col.accent,
          "click": opt.col.flavour,
        },
        blur = {
          "idle": 7,
          "hover": 2,
          "click": 2,
        },
      ),
    )

    self.anim.col = ui.col.text.idle
    self.anim.alpha = util.Alpha("upper", bounds = (16, 64))
    self.anim.blur = self.style.blur["idle"]
    self.anim.blurred = self.anim.blur - 1
    self.anim.cover = self.cover
    self.anim.shade = py.Surface(self.size)
    self.anim.shade.fill(0x00000)

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
      (ui.size.select.series[1] + 50)
    * list(levels.charts.keys()).index(self.series)
    )

  def render(self):
    interact = super().interact()
    self.anim.col = self.style.cols[interact]
    self.anim.blur = self.style.blur[interact]
    self.anim.alpha.alt(config.faderate if interact == "idle" else -config.faderate)

    # This approaches asymptotically, so we have to stop at some point
    if abs(self.anim.blurred - self.anim.blur) > 0.1:
      self.anim.blurred = util.slide(self.anim.blurred, self.anim.blur)
      self.anim.cover = effects.blur.blur(self.cover, self.anim.blurred)

    self.surf.blit(
      source = self.anim.cover,
      dest = (0, 0),
      area = py.Rect(
        (self.cover.get_width() - self.rect.width) / 2,
        (self.cover.get_height() - self.rect.height) / 2,
      *self.size)
    )

    # darken image
    self.anim.shade.set_alpha(self.anim.alpha())
    self.surf.blit(self.anim.shade, [0, 0])

    rendered = Text.render(self.series.upper(),
      style = Text.Style(typeface = "title", size = 50, col = self.anim.col)
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

    Object.__init__(self,
      track = track,
      size = ui.size.select.track,
      cover = util.find.asset(f"covers/{cover or 'none.png'}"),
      locktext = locktext,
      root = roots.select("track", track),
      style = Element.Style(
        cols = {
          "idle": ui.col.text.idle,
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
      (ui.size.select.track[1] + 50)
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
