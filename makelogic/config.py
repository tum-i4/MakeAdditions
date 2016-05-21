"""
Load global configurations, if they exist in a config.ini file
"""

import configparser
CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

CLANG = CONFIG.get("toolchain", "clang", fallback="clang")
LLVMLINK = CONFIG.get("toolchain", "llvmlink", fallback="llvm-link")
