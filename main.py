'''
Algorhythm
A rhythm game made in pygame!
'''

import sys

import pygame as py
from pygame.locals import *

from core import game, level, screen, sprites, ui, config
import util

from splash import splash
from levels import levels

## NOTE testing
from time import time
tick = time()
diffs = []
###


class main:
  '''Main functions that control the game.'''
  
  def events():
    '''Handle major game events.
    
    Events for each frame are stored in the global `game.events`, for all sprites to access and handle accordingly.
    '''

    game.events = py.event.get()
    
    for event in game.events:
      if event.type == QUIT:
        game.state = None
        return
      
      elif event.type == KEYDOWN:
        key = event.key
        game.keys.append(key)
        
        if key == K_ESCAPE:
          main.pause()

        ## NOTE testing
        elif key == K_SPACE:
          print(level.beat); break
          global tick, diffs
          now = time()
          diff = now - tick
          diffs.append(diff)
          if len(diffs) > 1:
            av = sum(diffs[1:]) / len(diffs[1:])
            print(f"diff = {diff}, average = {av}, bpm = {60 / av}")
          tick = now
        ###

      elif event.type == KEYUP:
        try:
          game.keys.remove(event.key)
        except ValueError:
          pass
    
    activate = util.index(game.keys, K_LCTRL, K_RCTRL, check = True)

    if activate:
      idx, ctrl = activate
      
      # only activate a key combo if a key is pressed after the ctrl key
      if idx < len(game.keys) - 1:
        action = game.keys[idx + 1]

        # remove pressed keys from history to prevent further unintentional combos
        game.keys.pop(idx + 1)
        game.keys.pop(idx)

        if action == K_w:
          game.state = None
          return
        
        elif action == K_SPACE:
          main.pause()

  def control():
    '''Control active game loop.'''

    if not screen.fade:
      sprites.splash[screen.state].update()
      if game.level and not screen.switch:  # NOTE `screen.switch` needed?
        game.level.run()
      
      if screen.switch:
        screen.fade = "OUT"
    
    elif screen.fade == "DARK":
      sprites.splash[screen.state].update()
      sprites.splash[screen.switch].update()
      
      screen.state = screen.switch
      screen.switch = None
      
      # update screen change history
      if len(screen.track) > 1:
        if screen.state == screen.track[-2]:
          screen.track.pop()
      else:
        screen.track.append(screen.state)
      
      screen.fade = "IN"
    
    else:
      sprites.fade.update()

  def hold():
    '''Control game while paused.'''

    if game.state:
      game.state -= 1
      if game.state < 1:
        game.state = True
        py.mixer.music.unpause()

    sprites.fade.update()
    sprites.pause.update()

  def render():
    '''Update screen.'''

    display.fill(ui.col.back)
    sprites.active.draw(display)
    py.display.flip()

  def pause():
    '''Pause or unpause the game.'''

    if game.level:
      if game.state:
        game.state = False
        py.mixer.music.pause()
      else:
        game.state = round(256 / config.faderate) + 1


## setup
py.init()
display = py.display.set_mode(screen.size, py.FULLSCREEN)

splash.setup()
splash.loadsequence(display)


## loop
while game.state is not None:
  main.events()
  
  if game.state is None:
    break
  elif game.state is True:
    main.control()
  else:
    main.hold()
  
  # game.pulse.tick(config.framerate)
  main.render()


## end
py.quit()

# keep window open in IDLE for testing
if "idlelib.run" not in sys.modules:
  sys.exit()
