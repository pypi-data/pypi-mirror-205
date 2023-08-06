import os
import sys
#sys.path.insert(1, 'mammopy/segmentation_models')
sys.path.append(os.path.dirname(os.path.abspath('mammopy')))
__version__ = "0.0.5"

from .mammopy import *
from .segmentation_models import *
from .visualization import canny_edges