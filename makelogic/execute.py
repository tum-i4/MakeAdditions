"""
Function for execute commands on the underlying OS
"""

from functools import wraps
from os.path import dirname, isfile
from os import chdir, environ, getcwd, sep
from subprocess import call, check_output, STDOUT
from shlex import quote
from typing import Sequence


def makefile_execution(func):
    """
    Small decorator for preparing and checking the environment to call make
    """
    @wraps(func)
    def wrapper(makefile: str, targets: Sequence[str]):
        """ Wrapper for the makefile environment"""

        # Target list is required
        if not targets:
            raise ValueError("Unknown target")

        # at first some input sanitizing
        check_makefile(makefile)
        targets = [quote(t) for t in targets]

        # save the current directory for returning to it later
        cwd = getcwd()

        # change to the directory of the makefile
        chdir(dirname(makefile))

        # Execute the decorated function
        result = func(makefile, targets)

        # return to the previous directory
        chdir(cwd)

        return result
    return wrapper


@makefile_execution
def run_make_with_debug_shell(_: str, targets: Sequence[str]) -> str:
    """ Run make and add all executed shell commands to the output """

    output = check_output(
        'make --print-directory --quiet SHELL="sh -x" ' + " ".join(targets),
        env=english_environment(), shell=True, stderr=STDOUT)

    # finally return the decoded output of make
    return output.decode()


@makefile_execution
def has_make_something_todo(_: str, targets: Sequence[str]) -> bool:
    """ Check, if the make command actually does something """
    return call(["make", "--question"] + targets) != 0


def english_environment():
    """
    Create a new environment with English language
    Thereby the later parsing is deterministic
    """

    english = dict(environ)
    english['LANG'] = 'en_US.UTF-8'
    return english


def check_makefile(makefile: str):
    """ Several check, if the given makefile is valid makefile and exists """
    if not isfile(makefile):
        raise FileNotFoundError("No such makefile")
    if not makefile.endswith(sep + "Makefile"):
        raise FileNotFoundError("No Makefile given")
