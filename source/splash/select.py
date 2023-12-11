'''
Implements the `SeriesSelect` and `TrackSelect` classes for selecting series or tracks.
'''

import pygame as pg

from core import screen, sprites, ui, opt
from innate import Val
import util

from splash import roots
from splash.elements import Element, Displayed
from splash.text import Text

from levels import levels

import effects.blur


class Select(Element):
  '''A stylised button with an image background.'''

  class Style:
    '''A selector style.'''

    def __init__(self, *, col = None, alpha = None, blur = None):
      '''Create a selector style.
      
      | parameter | type | description |
      | :-------- | :--- | :---------- |
      | `col` | `dict[str: Color]` | Text colour. |
      | `alpha` | `dict[str: num]` | Opacity of darkness cover. |
      | `blur` | `dict[str: num]` | Radius of image blur. |

      Each argument is a `dict`, with the keys being the 4 interaction states `'idle'`, `'hover'`, `'click'`, `'lock'`
      '''

      self.cols = {
        "idle": ui.col.text.idle, "hover": opt.col.accent,
        "click": opt.col.flavour, "lock": ui.col.text.lock,
      }
      self.alpha = {"idle": 32, "hover": 32, "click": 96, "lock": 192}
      self.blur = {"idle": 10, "hover": 4, "click": 4, "lock": 15}
      
      # Override defaults by whichever settings have been specified
      self.cols.update(col or {})
      self.alpha.update(alpha or {})
      self.blur.update(blur or {})


  def __init__(self, id, size, cover, locktext, display):
    '''Create a selector element.'''

    super().__init__(id = id, anim = True, interact = True, display = display)

    self.size = size
    surf = util.find.asset(f"covers/{cover}", "covers/none.png")
    self.cover = util.resize(surf, size).convert_alpha()
    self.locktext = locktext
  
  def _centre_(self, surf, rect) -> pg.Rect:
    '''Internal utility method to get centered area of a pygame Surface.'''

    return pg.Rect(
      (surf.get_width() - rect.width) / 2,
      (surf.get_height() - rect.height) / 2,
      *self.size
    )

  def update(self):
    self.surf = pg.Surface(self.size, pg.SRCALPHA)
    self.rect = self.surf.get_rect()
    
    self.position()
    super().position()

    if self.display.lock():
      self.lock()
    else:
      self.render()

  def render(self):
    '''Rounds the corners of the button.'''

    surf = pg.Surface(self.size, pg.SRCALPHA)
    pg.draw.rect(surf,
      color = [255, 255, 255],
      rect = (0, 0, *self.size),
      border_radius = round(min(self.size) * ui.radius / 2)
    )
    self.surf.blit(surf, (0, 0), special_flags = pg.BLEND_RGBA_MIN)


class SeriesSelect(Select):
  '''A selector for selecting a series in the series selection menu.'''

  def __init__(self, id,
    series,
    cover = None,
    lock = None,
    locktext = None,
    style = None,
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

    super().__init__(id = id,
      size = ui.size.select.series,
      cover = cover,
      locktext = locktext,
      display = Displayed(
        show = {"select"},
        align = (0, -1),
        scroll = (lambda: screen.scroll["select"]()),
        layer = "splash",
        lock = lock,
      ),
    )

    self.series = series
    self.root = roots.switch.state(f"select.{series.lower()}")
    self.style = style or Select.Style()

    self._anims_()

  def _anims_(self):
    '''Internal utility method to initialise animation attributes.'''

    self.anim.col = ui.col.text.idle
    blurs = list(self.style.blur.values())[:3]
    self.anim.blur = Val("upper", lower = min(blurs), upper = max(blurs))
    self.anim.alpha = util.Alpha("upper")

    self.anim.shade = pg.Surface(self.size)
    self.anim.shade.fill(0x00000)
    self.anim.cover = None
    self.anim.covers = {**{
      each: effects.blur.blur(self.cover, each)
      for each in range(self.anim.blur.lower, self.anim.blur.upper + 1)
    }, **{
      self.style.blur["lock"]:
      effects.blur.blur(self.cover, self.style.blur["lock"])
    }}

  def position(self):
    self.x = util.cord(x = 0)[0]
    self.y = (50 +
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
      self.surf.blit(self.anim.shade, (0, 0))

    rendered = Text.render(self.series.upper(),
      style = Text.Style(typeface = "title", size = 50, col = self.anim.col)
    )
    self.surf.blit(rendered[0],
      dest = util.root(rendered[1], self.size[0] / 2, self.size[1] / 2)
    )

    super().render()

  def lock(self):
    self.surf.blit(
      source = self.anim.covers[self.style.blur["lock"]],
      dest = (0, 0),
      area = self._centre_(self.cover, self.rect)
    )

    self.anim.shade.set_alpha(self.style.alpha["lock"])
    self.surf.blit(self.anim.shade, (0, 0))

    if self.locktext:
      rendered = Text.render(self.locktext,
        style = Text.Style()
      )
      self.surf.blit(rendered[0],
        dest = util.root(rendered[1], self.size[0] / 2, self.size[1] / 2)
      )

    super().render()


class TrackSelect(SeriesSelect):
  '''Represents a stylised button for selecting a track in the track selection menu.'''

  def __init__(self, id,
    series,
    track,
    cover = None,
    lock = None,
    locktext = None,
    style = None,
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

    super(SeriesSelect, self).__init__(id = id,
      size = ui.size.select.track,
      cover = cover,
      locktext = locktext,
      display = Displayed(
        show = {display},
        align = (0, -1),
        scroll = (lambda: screen.scroll[display]()),
        layer = "splash",
        lock = lock,
      ),
    )

    self.series = series
    self.track = track
    self.root = roots.select("track", track)
    self.style = style or Select.Style()

    super()._anims_()

  def position(self):
    self.x = util.cord(x = -0.35)[0]
    self.y = (50 +
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
      style = Text.Style(typeface = "title", size = 40, col = self.anim.col)
    )
    self.surf.blit(rendered[0],
      dest = util.root(rendered[1], 25, self.size[1] - 25, align = (-1, 1))
    )

    if not self.track.artist:
      return

    rendered = Text.render(self.track.artist,
      style = Text.Style(size = 25, col = self.anim.col)
    )
    self.surf.blit(rendered[0],
      dest = util.root(rendered[1], 25, 25, align = (-1, -1))
    )

    super(SeriesSelect, self).render()
