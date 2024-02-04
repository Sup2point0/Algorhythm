'''
Execute this file to run the game!
'''

import sys

import pygame as pg


if __name__ == "__main__":
  # import first to initialise the display as early as possible
  import core

  # then load the rest, which takes some time
  from Algorhythm import main
  from splash import splash, sequence

  splash.load()
  sequence.load(skip = True)  ## NOTE dev

  # main loop
  while core.game.state is not None:
    main.events()
    
    if core.game.state is None:
      break
    elif core.game.state is True:
      main.control()
    else:
      main.hold()
    
    main.render()

  pg.quit()

  ## NOTE keep window open in IDLE for testing
  if "idlelib.run" not in sys.modules:
    sys.exit()
