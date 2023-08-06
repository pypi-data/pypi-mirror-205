# read version from installed package
from importlib.metadata import version
__version__ = version("rtichoke")
from rtichoke.discrimination.roc import create_roc_curve
