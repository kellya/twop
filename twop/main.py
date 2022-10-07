import sys
import os
from . import twop

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path + "/../")


twop.main()
