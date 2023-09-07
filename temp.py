@ extend
class Element:
  def __init__(self, id, pos = None, display = None, *args, **kwargs):
    self.id = id
    self.pos = pos or [0, 0]
    self.display = display or []


@ level/effects.py
class PopEffect(py.sprite.Sprite):
  '''A class to contain the component sprites that make up the animated effect when a note is hit.'''

  def __init__(self, pos, acc = "hit", size = None, speed = None):
    '''Create a note hit effect.

    | argument | type | description |
    | :------- | :--- | :---------- |
    | `pos` | `(num, num)` | The position to create the effect. |
    | `acc` | `str` | The accuracy of the hit, which affects effect appearance. |
    | `size` | `num` | The greatest the radius of the circles involved in the effect will be. |
    | `speed` | `(int, num)` | How quickly the effect vanishes. The first value represents how many frames will pass before it starts fading, the second how much transparency will increase per frame. |
    '''

    super().__init__(sprites.effects)
    sprites.active.add(self, layer = 2)  # NOTE?

    self.pos = pos
    self.col = ui.col.perfect if acc == "perfect" else ui.col.hit
    self.size = size or ui.effect.popsize
    self.speed = speed or opt.effect.speed

    class anim:
      tick = 0
      alpha = util.Alpha(192)
      pop = self.size
      poof = 1
      boop = 1

    self.anim = anim

  def update(self):
    self.anim.tick += 1

    ## animate
    if self.anim.tick > opt.effect.speed[0]:
      self.anim.alpha.alt(-opt.effect.speed[1])
    if self.alpha.value == 0:
      return self.kill()

    self.anim.pop = util.slide(self.anim.pop, 1, 2)
    self.anim.poof = util.slide(self.anim.poof, self.size, 2)
    self.anim.boop = util.slide(self.anim.boop, self.anim.poof, 2)

    ## render
    self.image = py.Surface([self.size] * 2, py.SRCALPHA)
    self.rect = self.image.get_rect()
    self.rect.topleft = self.pos
    py.draw.circle(
      surface = self.image,
      radius = self.anim.pop
      ...,
      width = 0,
    )
    py.draw.circle(
      surface = self.image,
      radius = self.anim.poof,
      ...,
      width = self.anim.poof - self.anim.boop,
    )


@ splash/switch.py
class Switch(Element):
  '''A switch button that can be enabled or disabled.'''

  def __init__(self, id, pos, root, display = list()):
    '''Create a switch button.

    | argument | type | description |
    | :------- | :--- | :---------- |
    | `id` | `str` | ... |
    | `pos` | `(num, num)` | ... |
    | `root` | `Callable` | The function to call when the button is switched (note: the changed state of the switch will be passed as an argument). |
    | `display` | `list[str]` | ... |
    '''

    super().__init__(id = id, pos = pos, display = display)

    self.state = False
    self.root = root

    class anim:
      x = 0

    self.anim = anim

  def update(self):
    # TODO click code
    if clicked:
      self.state = not self.state
        self.root(self.state)

    self.image = py.Surface(ui.size.switch, py.SRCALPHA)
    py.draw.rect(
      surface = self.image,
      rect = py.Rect([0, 0], ui.size.switch),
      ...,
      width = 2,
      border_radius = (ui.size.switch[1] + 10) // 2,
    )  # NOTE?

    offset = 0.25 if self.state else -0.25
    py.draw.circle(
      surface = self.image,
      pos? = util.root(
        py.Rect([rad, rad], ui.size.switch),
        x = ui.size.switch[0] / 2 + offset * (ui.size.switch[0] - ui.size.switch [1]) / 2,
        y = ui.size.switch[1] / 2
      ),
      radius = ui.size.switch,
      ...,
      width = 0,
    )

    self.rect = self.image.get_rect()
    self.rect.topleft = util.root(self.rect, *self.pos)  # NOTE?


@ splash.tabs
class Tab(py.sprite.Sprite):
  '''A tab within a `TabView`.'''

  def __init__(self, id, size, lock, text, style = None):
    '''Create a tab to add to a `TabView`.

    | argument | type | description |
    | :------- | :--- | :---------- |
    | `id` | `str` | Unique identifier for the tab. When the tab is selected, the variable linked to the tabber is set to this `id`. |
    | `lock` | `Callable` | Function called to check if tab should be enabled or disabled. |
    '''

    self.id = id
    self.size = size
    self.text = text
    self.style or buttons.Style()

  def control(root: TabView, idx):
    '''Process tab functionality.'''

    self.rect = py.Rect(
      root.rect.x + sum(tab.size[0] for tab in root.tabs[:idx]),
    0, self.size)
    self.rect.y = util.root(self.rect, y = root.rect.y)[1]

    # TODO hover and click with collision


class TabView(Element):
  '''A collection of buttons to switch between tabs.'''

  def __init__(self, id, pos, tabs: list[Tab], display = None, edge = "round"):
    '''Create a tabber.

    | argument | type | description |
    | :------- | :--- | :---------- |
    | `tabs` | `list[Tab]` | List of tabs to add to the tabber, in order. |
    | `edge` | `str` | Edge style – can be `round`, `sharp`, or `angular`. |
    '''

    super().__init__(id = id, pos = pos, display = display)

    self.tabs = py.sprite.Group(tabs)

    self.image = py.Surface([
      sum(tab.size[0] for tab in self.tabs),
      max(tab.size[1] for tab in self.tabs),
    ], py.SRCALPHA)
    self.rect = self.image.get_rect()

  def update(self):
    ...

    self.rect.topleft = util.root(self.rect, *self.pos)

    for i, tab in enumerate(self.tabs):
      tab.process(self, i)


@ roots.py
def switchstate(var: str):
  '''...'''

  def root(state):
    globals()[var] = state

  return root


~~~


@ util.py
def overwrite(file, content: str):
  '''Overwrite a JSON file with `content`.'''

  file.seek(0)
  file.write(json.dumps(content, indent = 0))
  file.truncate()


@ process/account.py
import json
import hashlib

class UsernameError(Exception):
  pass

class PasswordError(Exception):
  pass

class Account:
  '''Represents a player account.'''

  def __init__(self, username: str, password: str):
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

    with open("process/data.json", "r+") as file:
      data = json.load(file)

      if user in data:
        raise UsernameError("Username is taken.")

      key = hashlib.sha256("sup" + password).hexdigest()

      self.data = {
        "user": user,
        "key": key,
        "opt": {dict(?)},
        "charts": {},
        "achievements": [each.id for each in game.achievements if each.unlocked],
      }
      data[user] = self.data
      util.overwrite(file, data)

    game.player = self

  def save(self):
    '''Save current player data to file.

    Should ideally be called after any modification(s) to ensure maximum synchronisation.
    '''

    with open("process/data.json", "w+") as file:
      data = json.load(file)
      data[self.data.user] = self.data
      util.overwrite(file, data)

  @ classmethod
  def login(username: str, password: str):
    '''Attempt to login to a player account.'''

    user = str(username).strip()
    if len(user) < 1:
      raise UsernameError("No username input.")
    key = str(password)
    if len(key) < 1:
      raise PasswordError("No password input.")

    with open("process/data.json", "r") as file:
      data = json.load(file)

      if user not in data:
        raise UsernameError("No account exists with this username.")
      if hashlib.sha256("sup" + key).hexdigest() != data[user]["key"]:
        raise PasswordError("Incorrect password.")

      game.player = self


@ process/achievement.py
class Achievement:
  '''Represents an in-game achievement.'''

  def __init__(self, id, name = None, secret = False, root = None):
    '''Create an achievement.'''

    self.id = id
    self.name = name or "Achievement Unlocked!"
    self.unlocked = False
    self.secret = secret
    self.root = root or lambda: None


@ process/achievements.py
'''
Achievements functionality
'''

from core import game.achievements

from process.achievement import Achievement


def init():
  '''Load game achievements (and sync if player is signed in).'''

  game.achievements = [
    Achievement(
      id = "",
      name = "Secret Algorithm",
      secret = True,
      root = lambda: level.hit = 0,
    ),
  ]

  if game.player:
    for each in game.achievements:
      if each.id in game.player.achievements:
        each.unlocked = True

def update() -> list[Achievement]:
  '''Check for unlocked achievements and return a list of them, if any.'''

  unlocked = []

  for each in game.achievements:
    if not each.unlocked:
      if each.root():
        each.unlocked = True
        unlocked.append(each)

  return unlocked


# TODO
buttons.Style(col = ["lock"], edge = ["sharp", "angular"])
self.anim.fade: bool -> splash.Element(fade animation)
