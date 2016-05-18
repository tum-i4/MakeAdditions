from .executer import dryRunMakefile
from .parser import splitInCommands, translateMakeAnnotations
from os import linesep


class MakeScript:

    """
    The .sh-script representation of the tasks from a Makefile
    """

    cmds = []

    def __init__(self, makefile: str, target: str = 'all'):
        self.cmds = translateMakeAnnotations(
            splitInCommands(dryRunMakefile(makefile, target)))

    def __str__(self):
        return "#!/bin/sh" + (linesep * 2) + linesep.join(self.cmds)
