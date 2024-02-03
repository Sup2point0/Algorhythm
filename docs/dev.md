# Dev Notes

Just development-related notes ^v^


<br>


## Tasks

### Ongoing
- Update button styles
- Add sliders
- Add chart details view

### Todo
- Generate actions when loading level to avoid iteration (DONE?)
- Rework screen state change to allow animation specification
- Selection and navigation history
- Rework load sequence

### Ideas
- Musical sound effects on button click
- Techy node background with floating geometric entities
  - Blue theme
  - Glow effects with Pillow
- `ColourPicker`, `KeyPicker`


<br>


## Precedence

Standardising orders to help maintain consistency while coding.

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
from innate import Object
from innate import Val
from innate import Alpha
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
):
  super().__init__(id, pos, anim = True, interact = True, display = ...)
```

<!-- this file is just for me, btw -->
