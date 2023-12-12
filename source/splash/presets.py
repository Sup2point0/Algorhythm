'''
Implements style and display presets.
'''

from core import ui

from splash import roots
from splash.elements import Displayed
from splash.text import Text


class style:
  '''Style setting presets.'''

  title = Text.Style(
    typeface = ui.font.title,
    size = 40,
  )


class display:
  '''Display setting presets.'''

  start = Displayed(
    show = {"start"},
    align = (-1, 0),
  )

  credits = Displayed(
    show = {"settings.credits"},
    scroll = {roots.scroll("settings.credits")},
  )
