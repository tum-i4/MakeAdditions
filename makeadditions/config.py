"""
Load global configurations, if they exist in a config.ini file
"""

import configparser
from os import path
from .execute import (
    check_llvm_config, check_opt, check_opt_delete,
    check_clang, check_llvmlink, read_binary_directory)

CONFIG = configparser.ConfigParser()
CONFIG.read(path.join(path.dirname(__file__), "..", "config.ini"))

LLVMCONFIG = path.expanduser(
    CONFIG.get("toolchain", "llvm-config", fallback="llvm-config"))
OPTDELETE = path.expanduser(CONFIG.get("toolchain", "optdelete", fallback=""))

LLVMBINDIR = read_binary_directory(LLVMCONFIG)
CLANG = path.join(LLVMBINDIR, "clang")
LLVMLINK = path.join(LLVMBINDIR, "llvm-link")
LLVMOPT = path.join(LLVMBINDIR, "opt")


def check_config():
    """ Check config variables are valid for exection """
    check_llvm_config(LLVMCONFIG)
    check_clang(CLANG)
    check_llvmlink(LLVMLINK)
    check_opt(LLVMOPT)
    check_opt_delete(LLVMOPT, OPTDELETE)
