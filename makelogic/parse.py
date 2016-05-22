"""
Helpful functions for string and command parsing
"""

from typing import Sequence
from os import linesep
import re
from .constants import MAKEANNOTATIONHINT


def extract_debugshell_and_makefile(makeoutput: str) -> Sequence[str]:
    """
    Extract a list of commands, that are logged in shell debug output,
    and annotations of the makefile from output of a make run
    """

    result = []

    # Each line can be a relevant command
    for line in makeoutput.splitlines():

        if line.startswith("make"):
            # extract make annotations
            result.append(line)

        elif line.startswith("+"):
            # extract shell debug output
            match = re.search(r"\++ (?P<command>.*)", line)
            result.append(match.group("command"))

    return result


def translate_makeannotations(makeoutput: Sequence[str])-> Sequence[str]:
    """
    Translate all the annotations of the Makefile-Output to executable commands
    """

    # makeoutput must start with directory information - the flag was given
    if (not makeoutput or
            not makeoutput[0].startswith("make: Entering directory ")):
        raise Exception("Directory changes cannot be recognized")

    # Manage the directories with a stack
    dirstack = []
    result = []

    for cmd in makeoutput:
        if cmd.startswith("make"):
            # If the command belongs to make itself

            # Look for a directory action
            match = re.search(r"^make(\[\d+\])?: (?P<action>Entering|Leaving) "
                              r"directory '(?P<dir>[^']*)'$", cmd)

            if match:
                # It's a directory action

                if match.group('action') == 'Entering':
                    dirstack.append(match.group('dir'))
                    result.append(
                        "cd " + match.group('dir') + MAKEANNOTATIONHINT)

                elif match.group('action') == 'Leaving':
                    lastdir = dirstack.pop()
                    result.append("cd " + lastdir + MAKEANNOTATIONHINT)
                continue

            # Look for a target with nothing to to
            match = re.search(r"make(\[\d+\])?: Nothing to be done for "
                              r"'(?P<target>[^']+)'", cmd)
            if match:
                # It's a nothing to do notice
                result.append(
                    "# make does nothing for " + match.group("target"))
                continue

            # Maybe not everything is supported (yet) ;(
            raise Exception("Unsupported make command: " + cmd)

        else:
            result.append(cmd)

    return result
