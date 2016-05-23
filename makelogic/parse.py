"""
Helpful functions for string and command parsing
"""

import os
import re
from typing import Sequence
from .constants import MAKEANNOTATIONHINT


class MakefileDirstack():
    """
    Helper class for transforming the entering and leaving directory
    annotations of make output to corresponding cd commands
    """

    def __init__(self):
        # Stack is needed to define, where we are after leaving
        self.dirstack = [os.getcwd()]

    def translate_if_dirannotation(self, cmd: str):
        """
        Transform make directory annotation and leave the rest untouched
        """

        if not cmd.startswith("make"):
            # Just looking for make annotations
            return cmd

        # Look for a directory action
        match = re.search(r"^make(\[\d+\])?: (?P<action>Entering|Leaving) "
                          r"directory '(?P<dir>[^']*)'$", cmd)

        # It's a directory action
        if match:

            if match.group('action') == 'Entering':
                self.dirstack.append(match.group('dir'))
                return "cd " + match.group('dir') + MAKEANNOTATIONHINT

            elif match.group('action') == 'Leaving':
                self.dirstack.pop()
                return "cd " + self.dirstack[-1] + MAKEANNOTATIONHINT

        # return other commands unmodified
        return cmd


def is_noop(cmd: str) -> bool:
    """ Checks, if the given command perform no operation, e.g. pure
    comment strings or all sorts of empty strings """
    return not cmd.strip() or cmd.strip().startswith("#")


def extract_debugshell(makeoutput: Sequence[str]) -> Sequence[str]:
    """ Extract all command invocations from shell debug statements and
    make them to normal commands """
    return [line.lstrip("+ ") for line in makeoutput]


def get_relevant_lines(makeoutput: str) -> Sequence[str]:
    """ Remove everything from make output, that is not a makefile annotation
    and shell debug output, but leaves the + sign in front of them """
    return [line for line in makeoutput.splitlines()
            if line.startswith("make") or line.startswith("+")]


def translate_to_commands(makeoutput: str) -> Sequence[str]:
    """ Translate all the output from make, debug-shell and output of commands
    during make, and translate them to executable commands """

    return extract_debugshell(
        translate_makeannotations(
            get_relevant_lines(makeoutput)))


def check_debugshell_and_makefile(makeoutput: str):
    """
    Check if the Makefile output can be parsed and transformed automatically.
    Raises exceptions, if something looks weird
    """

    # makeoutput must start with directory information.
    # Reason: The --print-directory flag for make flag was given
    if (not makeoutput or
            not makeoutput.startswith("make: Entering directory ")):
        raise Exception(
            "Directory changes cannot be recognized: " + makeoutput[0:35])


def translate_makeannotations(makeoutput: Sequence[str])-> Sequence[str]:
    """
    Translate all the annotations of the Makefile-Output to executable commands
    """

    dirstack = MakefileDirstack()

    makepatterns = (
        # Message, if the target is already completed
        r"^make(\[\d+\])?: Nothing to be done for '[^']+'$",

        # start working on a subtarget
        r"^make (?P<target>[\w-]+)$",
    )

    return [
        "# " + cmd + MAKEANNOTATIONHINT
        if cmd.startswith("make") and any(
            re.search(pattern, cmd) for pattern in makepatterns)
        else dirstack.translate_if_dirannotation(cmd)
        for cmd in makeoutput
    ]
