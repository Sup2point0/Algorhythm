'''
Handles dynamic splash functionality through the `run` function.
'''

from core import game, screen, sprites, config
import util

from splash.select import TrackSelect


@ util.log(log = {None, *game.select.values()})
def run():
  '''Handle dynamic splash functionality for more interactive screens.'''

  if screen.state.startswith("select."):
    process.trackselect()


class process:
  def trackselect():
    '''Sort track selector elements, only if necessary.'''

    data = {screen.state, *game.select.values()}
    if run.log == data:
      return

    run.log = data
    sprites.splash["select.tracks"] = [
      each.id for each in sorted(
        [
          sprite for sprite in sprites.splash[screen.state]
          # if isinstance(sprite, TrackSelect)
        ],
        key = config.sorts[game.select["sort"]],
        reverse = game.select["reverse"],
      )
    ]
