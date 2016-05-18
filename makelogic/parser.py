from typing import Sequence
from os import linesep


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
