'''
Level events
'''


class Action:
  '''An event that can be triggered within a level.'''

  def __init__(self, beat, action, loop = None):
    '''Create an action event.
    
    | parameter | type | description |
    | :-------- | :--- | :---------- |
    | `beat` | `num` | Beat on which event should occur. |
    | `action` | `Callable` | Function called when event occurs. |
    | `loop` | `int, num` | How many times to loop the action, and the gap in beats between each repeat. |
    '''

    self.beat = beat
    self.activate = action
    self.loop = loop
    self.looped = 0


class Hint(Action):
  '''Text that displays during a level.'''
  
  def __init__(self, *args, **kwargs):
    '''Create a level hint.
    '''

    super().__init__(*args, **kwargs)
