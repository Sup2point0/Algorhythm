'''
Implements the `Account` class for managing player accounts.
'''

import json
import hashlib

from core import game, opt
from innate import Val
import util


class UsernameError(Exception):
  pass

class PasswordError(Exception):
  pass


def _construct_(source):
  '''An internal method to convert the namespace structure of `source` into a multi-level `dict`.'''

  out = {}
  struct = vars(source)

  for key in struct:
    if not key.startswith("_"):
      val = struct[key]
      if isinstance(val, Val):
        out[key] = val()
      elif hasattr(val, "__dict__"):
        out[key] = _construct_(val)
      else:
        out[key] = val

  return out


class Account:
  '''Represents a player account.'''

  def __init__(self, data: dict):
    '''Create a player account object.'''

    self.data = data

  @ classmethod
  def create(username: str, password: str):
    '''Create a new player account.'''

    user = str(username).strip()
    if len(user) < 1:
      raise UsernameError("No username input.")
    elif len(str(username)) == 69:
      raise UsernameError("Nice, but that username’s too long.")
    elif len(user) > 30:
      raise UsernameError("Username cannot exceed 30 characters.")

    key = str(password)
    if len(key) < 4:
      raise PasswordError("Password should be at least 4 characters.")
    elif len(key) > 60:
      raise PasswordError("That’s way, way too long for a password.")
    elif len(key) > 50:
      raise PasswordError("Some long password you got there...")
    elif len(key) > 40:
      raise PasswordError("Password cannot exceed 40 characters.")

    with open("access/data.json", "r+") as file:
      data = json.load(file)

      if user in data:
        raise UsernameError("Username is taken.")

      key = hashlib.sha256("sup" + password).hexdigest()
      
      data[user] = {
        "user": user,
        "key": key,
        "opt": {_construct_(opt)},
        "charts": {},
        "achievements": [each.id for each in game.achievements if each.unlocked],
        "stats": data["root"]["stats"],
      }

      game.player = Account(data[user])

      util.overwrite(file, data)

  def save(self):
    '''Save current player data to file.

    Should ideally be called after any modification(s) to ensure maximum synchronisation.
    '''

    with open("access/data.json", "w+") as file:
      data = json.load(file)
      data[self.data.user] = self.data
      util.overwrite(file, data)

  @ classmethod
  def login(cls, username: str, password: str):
    '''Attempt to login to a player account.'''

    user = str(username).strip()
    if len(user) < 1:
      raise UsernameError("No username input.")
    key = str(password)
    if len(key) < 1:
      raise PasswordError("No password input.")

    with open("access/data.json", "r") as file:
      data = json.load(file)

      if user not in data:
        raise UsernameError("No account exists with this username.")
      if hashlib.sha256("sup" + key).hexdigest() != data[user]["key"]:
        raise PasswordError("Incorrect password.")

      game.player = Account(data[user])

  def logout(self):
    '''Logout of the current player account.'''

    self.save()
    game.player = None

  @ property
  def achievements(self):
    '''A list of the IDs of the achievements the player has unlocked.'''

    return self.data["achievements"]