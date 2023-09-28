'''
Achievements management
'''

from core import game

from process.achievement import Achievement


def init():
  '''Load game achievements (and sync if player is signed in).'''

  game.achievements = [
    Achievement(
      id = "secrets.secret-algorithm",
      name = "Secret Algorithm",
      desc = "Play a level without hitting any notes",
      secret = True,
      root = lambda: level.hit == 0,
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

  if game.player:
    game.player.achievements.extend([each.id for each in unlocked])
    game.player.save()

  return unlocked
