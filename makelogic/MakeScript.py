from .execute import dryRunMakefile
from .parse import splitInCommands, translateMakeAnnotations
from os import linesep


class MakeScript:

    """
    The .sh-script representation of the tasks from a Makefile
    """

    # Header for the output of the makescript
    __HEADER = "#!/bin/sh" + (linesep * 2)

    def __init__(self):
        """ Just init an empty makefile """
        self.cmds = []

    @classmethod
    def from_makefile(cls, makefile, target=None):
        """ Alternative constructor from makefile on the filesystem """
        target = target or "all"

        # Start with an empty Makescript
        new = cls()

        # And add the commands of a dry run
        new.cmds = translateMakeAnnotations(
            splitInCommands(dryRunMakefile(makefile, target)))

        return new

    def __str__(self):
        return self.__HEADER + linesep.join(self.cmds)
