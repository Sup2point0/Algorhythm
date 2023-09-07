'''
Level events
'''


class Action:
  '''An event that can be triggered within a level.'''

  def __init__(self, beat, action):
    '''Create an event.
    
    | argument | type | description |
    | :------- | :--- | :---------- |
    | `beat` | `int`, `float` | The beat on which action should occur. |
    | `action` | `Callable` | The function to call when action occurs. |
    '''

    self.beat = beat
    self.activate = action


class Hint(Action):
  '''Text that displays during a level.'''
  
  def __init__(self, *args, **kwargs):
    '''Create a text hint.'''

    super().__init__(*args, **kwargs)
