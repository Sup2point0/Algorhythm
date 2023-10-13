# Notes

Just little notes to maintain consistency while coding ;)


### Import Precedence

```py
import sys
import math
import random
import json
import hashlib
import colorsys
from enum import Enum

import pygame as py
from pygame.locals import *
from PIL import ...

from core import game, level, screen, sprites, ui, config, opt
from innate.value import BoundValue (as Val)
from innate.object import Object
from innate.sprite import Sprite
import util

from splash.elements import ...
from splash.covers import ...
from splash.asset import ...
from splash.text import ...
from splash.buttons import ...
from splash.slider import ...

from level.hitline import ...
from level.lane import ...
from level.notes import ...
from level.action import ...

from levels import ...

from effects import ...
```

### Splash Sprite Parameter Precedence

```py
def __init__(self, id,
  pos, align,
  text, image,
  root,
  style, display
)
```
