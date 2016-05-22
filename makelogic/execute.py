"""
Function for execute commands on the underlying OS
"""

from os.path import dirname, isfile
from os import chdir, environ, getcwd, sep
from subprocess import CalledProcessError, check_output, STDOUT
from typing import Sequence


def dryrun_makefile(makefile: str, target: str="all") -> str:
    """ Perform a dry run on makefile with the given target and returns the
        output, i.e. all the commands necessary for the build """

    return run_make_with_commands(
        makefile, ["--dry-run", "--print-directory", target])


def run_make_with_debug_shell(makefile: str, target: str="all") -> str:
    """ Run make and add all executed shell commands to the output """

    # at first some input sanitizing
    if not isfile(makefile):
        raise FileNotFoundError("No such makefile")
    if not makefile.endswith(sep + "Makefile"):
        raise FileNotFoundError("No Makefile given")

    # save the current directory for returning to it later
    cwd = getcwd()

    # Create a new environment with English language
    # Thereby the later parsing is deterministic
    english = dict(environ)
    english['LANG'] = 'en_US.UTF-8'

    # change to the directory of the makefile
    chdir(dirname(makefile))

    # actually call make with given args on this file
    # TODO Exscape evil shell target
    output = check_output(
        'make --print-directory --quiet SHELL="sh -x" ' + target,
        env=english, shell=True, stderr=STDOUT)

    # return to the previous directory
    chdir(cwd)

    # finally return the decoded output of make
    return output.decode()


def has_make_something_todo(makefile: str, target: str="all") -> bool:
    """ Check, if the make command actually does something """

    try:
        # --question returns with non zero output, if something has to be done
        run_make_with_commands(makefile, ["--question", target])
    except CalledProcessError:
        # catch non zero return status
        return True
    return False


def run_make_with_commands(
        makefile: str, args: Sequence[str]=None, shell: bool=False):
    """ Run make on the given makefile with the given args """

    # Mutable default argumant for args
    args = args or []

    # at first some input sanitizing
    if not isfile(makefile):
        raise FileNotFoundError("No such makefile")
    if not makefile.endswith(sep + "Makefile"):
        raise FileNotFoundError("No Makefile given")

    # save the current directory for returning to it later
    cwd = getcwd()

    # Create a new environment with English language
    # Thereby the later parsing is deterministic
    english = dict(environ)
    english['LANG'] = 'en_US.UTF-8'

    # change to the directory of the makefile
    chdir(dirname(makefile))

    # actually call make with given args on this file
    output = check_output(['make'] + args, env=english)

    # return to the previous directory
    chdir(cwd)

    # finally return the decoded output of make
    return output.decode()
