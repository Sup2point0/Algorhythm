'''
Implements the `SeriesSelect` and `TrackSelect` classes for selecting series or tracks.
'''

import pygame as py

from core import screen, sprites, ui, opt
from innate import Val, Object
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
    _size_ = None,
    _display_ = None,
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

    super().__init__(id = id, anim = True, interact = True,
      display = _display_ or Displayed(
        show = {"select"},
        align = (0, -1),
        scroll = (lambda: screen.scroll["select"]()),
        layer = sprites.active.layer["splash"],
        lock = lock,
      ),
    )

    Object.__init__(self,
      size = _size_ or ui.size.select.series,
      series = series,
      cover = self._resize_(cover, _size_),
      locktext = locktext,
      root = roots.switch.state(f"select.{series.lower()}"),
      style = Element.Style(
        cols = {
          "idle": ui.col.text.idle, "hover": opt.col.accent,
          "click": opt.col.flavour, "lock": ui.col.text.lock,
        },
        alpha = {"idle": 32, "hover": 32, "click": 96, "lock": 192},
        blur = {"idle": 10, "hover": 4, "click": 4, "lock": 15},
      ),
    )

    self.anim.col = ui.col.text.idle
    blurs = list(self.style.blur.values())[:3]
    self.anim.blur = Val("upper", lower = min(blurs), upper = max(blurs))
    self.anim.alpha = util.Alpha("upper")

    self.anim.shade = py.Surface(self.size)
    self.anim.shade.fill(0x00000)
    self.anim.cover = None
    self.anim.covers = {**{
      each: effects.blur.blur(self.cover, each)
      for each in range(self.anim.blur.lower, self.anim.blur.upper + 1)
    }, **{
      self.style.blur["lock"]:
      effects.blur.blur(self.cover, self.style.blur["lock"])
    }}

  def _resize_(self, cover, size) -> py.Surface:
    '''Internal utility method to resize cover asset to suitable size.'''

    class root:
      surf = util.find.asset(f"covers/{cover or 'none.png'}")
      width, height = surf.get_size()

    width, height = size or ui.size.select.series
    if root.width / root.height < width / height:
      scale = width / root.width
    else:
      scale = height / root.height

    return py.transform.scale_by(root.surf, scale)
  
  def _centre_(self, surf, rect) -> py.Rect:
    '''Internal utility method to get centered area of a pygame Surface.'''

    return py.Rect(
      (surf.get_width() - rect.width) / 2,
      (surf.get_height() - rect.height) / 2,
      *self.size
    )

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
    self.anim.alpha.set(self.style.alpha[interact])
    self.anim.blur.alt(1 if interact == "idle" else -1)

    self.surf.blit(
      source = self.anim.covers[self.anim.blur()],
      dest = (0, 0),
      area = self._centre_(self.cover, self.rect)
    )

    # darken image
    if (alpha := self.anim.alpha()):
      self.anim.shade.set_alpha(alpha)
      self.surf.blit(self.anim.shade, [0, 0])

    rendered = Text.render(self.series.upper(),
      style = Text.Style(typeface = "title", size = 50, col = self.anim.col)
    )
    self.surf.blit(rendered[0],
      dest = util.root(rendered[1], self.size[0] / 2, self.size[1] / 2)
    )

  def lock(self):
    self.surf.blit(
      source = self.anim.covers[self.style.blur["lock"]],
      dest = (0, 0),
      area = self._centre_(self.cover, self.rect)
    )

    self.anim.shade.set_alpha(self.style.alpha["lock"])
    self.surf.blit(self.anim.shade, [0, 0])

    if self.locktext:
      rendered = Text.render(self.locktext,
        style = Text.Style()
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

    super().__init__(id, series, cover, lock, locktext,
      _size_ = ui.size.select.track,
      _display_ = Displayed(
        show = {display},
        align = (0, -1),
        scroll = (lambda: screen.scroll[display]()),
        layer = sprites.active.layer["splash"],
        lock = lock,
      )
    )

    Object.__init__(self,
      track = track,
      root = roots.select("track", track),
    )

  def position(self):
    self.x = util.cord(x = -0.5)[0]
    self.y = (100 +
      (ui.size.select.track[1] + 50)
    * sprites.splash["select.tracks"].index(self.id)
    )

  def render(self):
    interact = super().interact()
    self.anim.col = self.style.cols[interact]
    self.anim.alpha.set(self.style.alpha[interact])
    self.anim.blur.alt(1 if interact == "idle" else -1)

    self.surf.blit(
      source = self.anim.covers[self.anim.blur()],
      dest = (0, 0),
      area = self._centre_(self.cover, self.rect)
    )

    rendered = Text.render(self.track.name,
      style = Text.Style(typeface = "title", size = 20, col = self.anim.col)
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
