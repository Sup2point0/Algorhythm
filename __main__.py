'''
Execute this file to run the game!
'''

import sys

import pygame as py

from Algorhythm import main

import core

from splash import splash


if __name__ == "__main__":
  py.init()

  splash.setup()
  splash.load()

  while core.game.state is not None:
    main.events()
    
    if core.game.state is None:
      break
    elif core.game.state is True:
      main.control()
    else:
      main.hold()
    
    main.render()

  py.quit()

  # keep window open in IDLE for testing
  if "idlelib.run" not in sys.modules:
    sys.exit()
