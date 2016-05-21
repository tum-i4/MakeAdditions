from typing import Sequence
from os import linesep
import re


def commandEndsIn(line: str) -> bool:
    """ Checks, wether the command in line ends in this line
        or continues on the next line """
    return line[-1] != '\\'


def splitInCommands(text: str) -> Sequence[str]:
    """ Splits the commands in text to a list of commands """

    # Split the text in a list of lines
    lines = text.splitlines()

    # some temporary variables
    result = []
    cache = ""

    for l in lines:
        cache += l
        if commandEndsIn(l):
            # add the complete command to the result
            result.append(cache)
            cache = ""
        else:
            # merge multi line command in the cache
            cache += linesep

    return result


def is_multicommand(cmd: str) -> bool:
    """ Checks, if a command combines multiple instructions """
    return any(c in cmd for c in ["&&", "|", ";", ">", "<"])


def translateMakeAnnotations(makeOutput: Sequence[str])-> Sequence[str]:
    """
    Translate all the annotations of the Makefile-Output to executable commands
    """

    # makeOutput must start with directory information - the flag was given
    if (not makeOutput or
            not makeOutput[0].startswith("make: Entering directory ")):
        raise Exception("Directory changes cannot be recognized")

    # Manage the directories with a stack
    dirstack = []
    result = []

    # some helpfull landmarks
    cdtoken = " # from make"

    for cmd in makeOutput:
        if cmd.startswith("make"):
            # If the command belongs to make itself

            # Look for a directory action
            match = re.search("^make(\[\d+\])?: (?P<action>Entering|Leaving) "
                              "directory '(?P<dir>[^']*)'$", cmd)

            if match:
                # It's a directory action

                if match.group('action') == 'Entering':
                    dirstack.append(match.group('dir'))
                    result.append("cd " + match.group('dir') + cdtoken)

                elif match.group('action') == 'Leaving':
                    lastdir = dirstack.pop()
                    result.append("cd " + lastdir + cdtoken)

            else:
                # Maybe not everything is supported (yet) ;(
                raise(Exception("Unsupported make command: " + cmd))

        else:
            result.append(cmd)

    return result
