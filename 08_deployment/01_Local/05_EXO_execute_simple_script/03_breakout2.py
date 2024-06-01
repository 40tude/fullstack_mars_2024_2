# docker run -it -v "$(pwd):/home/app" jedha/simple-python-image -q

import random
import sys
from pathlib import Path

# import pandas as pd


print("Chemin de VSCode           : ", Path.cwd())

p = Path(__file__).parent
print("Chemin contenant le script : ", p)
