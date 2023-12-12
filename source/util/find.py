'''
Implements utility functions involving finding values or objects.
'''

import pygame as pg
import numpy as np
import librosa

from core import config, opt


def row(key) -> str:
  '''Find which row of the keyboard a key belongs to.'''

  rows = config.keys.__dict__
  for each in rows:
    if not each.startswith("_"):
      if key in rows[each]:
        return each
  else:
    return "spec"

def col(key):
  '''Find suitable colour for a game key.'''
  
  return vars(opt.col)[row(key)]

def asset(*files) -> pg.Surface:
  '''Load an image file to a pygame Surface.'''

  for file in files:
    try:
      return pg.image.load(f"assets/{file}")
    except:
      pass

def sync(file: str):  # NOTE needed?
  '''Find tempo and offset of a soundtrack audio file.'''

  print("syncing")  # NOTE testing

  wave, rate = librosa.load(file)
  tempo, beats = librosa.beat.beat_track(y = wave, sr = rate)
  frame = librosa.frames_to_time(beats, sr = rate)
  diff = np.mean(np.diff(frame))

  print(f"synced [tempo = {tempo}, offset = {frame[0] - diff}]")

  return {
    "tempo": tempo,
    "offset": frame[0] - diff,
  }
