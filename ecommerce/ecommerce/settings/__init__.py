
from ._base import *
from .production import *
try:
    from .dev import *
    
except :
    print('Pas de fichier dev.py')