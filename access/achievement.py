'''
Game achievements
'''


class Achievement:
  '''Represents a game achievement.'''

  def __init__(self,
    id: str,
    name = None,
    desc = None,
    secret = False,
    root = None
  ):
    '''Create an achievement.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `id` | `str` | Unique ID to identify achievement. |
    | `name` | `str` | Displayed name of achievement. |
    | `desc` | `str` | Description of achievement. |
    | `secret` | `bool` | Whether the achievement is a secret one. |
    | `root` | `Callable` | Function called to check if achievement should be unlocked. |
    '''

    if root is None:
      raise ValueError("Achievement root is required.")

    self.id = id
    self.name = name or "Achievement Unlocked!"
    self.desc = desc or "How is this unlocked again?"
    self.secret = secret
    self.root = root
    self.unlocked = False
