from os.path import dirname, basename, isfile
import glob

# Import all modules from this directory
# Needed for automatic transformer registration
modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f)]
