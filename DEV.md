# Dev Notes

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
import innate
from innate import Val
from innate import Object
from innate.sprite import Sprite
import util

from splash import roots
from splash.elements import ...
from splash.covers import ...
from splash.asset import ...
from splash.text import ...
from splash.buttons import ...
from splash.slider import ...
from splash.select import ...

from level.hitline import ...
from level.lane import ...
from level.notes import ...
from level.action import ...

from levels import ...

import effects.blur
from effects.shake import ...
from effects.pop import ...
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