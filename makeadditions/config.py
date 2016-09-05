"""
Load global configurations, if they exist in a config.ini file
"""

import configparser
from os import path
from .execute import check_clang, check_llvmlink

CONFIG = configparser.ConfigParser()
CONFIG.read(path.join(path.dirname(__file__), "..", "config.ini"))

CLANG = path.expanduser(CONFIG.get("toolchain", "clang", fallback="clang"))
LLVMLINK = path.expanduser(
    CONFIG.get("toolchain", "llvmlink", fallback="llvm-link"))
LLVMOPT = path.expanduser(CONFIG.get("toolchain", "llvmopt", fallback="opt"))
OPTDELETE = path.expanduser(CONFIG.get("toolchain", "optdelete", fallback=""))


def check_config():
    """ Check config variables are valid for exection """
    check_clang(CLANG)
    check_llvmlink(LLVMLINK)
