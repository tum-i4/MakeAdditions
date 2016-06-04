"""
Collection of constants for the different modules
"""

from .config import CLANG

# List of all compiler alias
COMPILERS = ["cc", "gcc", "clang", CLANG]

# All optimizer flags in the compiler
OPTIMIZERFLAGS = ['-O0', '-O1', '-O2', '-O3', '-Og', '-Os', '-Ofast']

# All flags for dependency generation
DEPENDENCYFLAGS = ["-MD", "-MMD", "-MP", "-M", "-MM"]

# All flags fro dependency emission
DEPENDENCYEMISSION = ["-MT", "-MF", "-MQ"]

# Add this comment commands from make annotations
MAKEANNOTATIONHINT = "from make"

# Additional file extension for executable files
# This may not be empty. ".bc" will be appended automatically
EXECFILEEXTENSION = ".x"
