# Dev Notes

Just little notes during development ^v^


<br>


## Precedence

To help maintain consistency while coding.

### Imports

```py
import sys
import math
import random
import json
import hashlib
import colorsys
from enum import Enum

import pygame as pg
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

### Splash Sprite Parameters

```py
def __init__(self, id,
  pos, align,
  text, image,
  root,
  style, display,
)
```


<br>


## Learnings

Little bits of knowledge picked up along the way, for anyone who might be looking to do the same.

- Git can’t stop tracking a file already being tracked, so you’ve gotta delete it and re-create it.
- VSCode executes code (at least for Python) with the directory open in Explorer as the current working directory.
  - We can configure it to execute from a particular directory with the `PYTHONPATH` variable in a `.env` file.
