"""
This class represents and stores the tasks and commands from a
Makefile (and a specific target). It can be printed as an .sh-script
"""

import re
from typing import Sequence
from os import linesep
from .execute import dryrun_makefile
from .parse import split_in_commands, translate_makeannotations


class MakeScript:

    """
    The .sh-script representation of the tasks from a Makefile
    """

    # Header for the output of the makescript
    __HEADER = "#!/bin/sh" + (linesep * 2)

    def __init__(self):
        """ Just init an empty makefile """

        # List for all commands
        self.cmds = []

        # Set of all used libraries
        self.libs = set({})

    def register(self, cmd: str):
        """ Extract and store informations needed by other commands """

        # look for generated libraries
        if cmd.startswith("ar cq "):
            libmatch = re.search(r"ar cq (\w+.a)", cmd)
            if libmatch:
                self.libs.add(libmatch.group(1) + ".bc")

    # pylint: disable=no-self-use
    def transform(self, cmd: str) -> str:
        """ Apply transformation to the vanilla command before it is stored """
        return cmd

    @classmethod
    def from_makefile(cls, makefile, target=None):
        """ Alternative constructor from makefile on the filesystem """
        target = target or "all"

        # Start with an empty Makescript
        new = cls()

        # collect the commands from a dryrun
        cmds = translate_makeannotations(
            split_in_commands(
                dryrun_makefile(makefile, target)))

        # store relevant information for later commands
        for cmd in cmds:
            new.register(cmd)

        # and store the translated commands
        new.cmds = [new.transform(cmd) for cmd in cmds]

        return new

    def __str__(self):
        """ Print the stored command as a .sh-script """
        return self.__HEADER + linesep.join(self.cmds)

    def append_cmd(self, cmd: str):
        """ Append a command to the internal command storage """

        # register the information of the command
        self.register(cmd)

        # and store the transformed command
        self.cmds.append(self.transform(cmd))

    def append_cmdlist(self, cmds: Sequence[str]):
        """
        Append all commands from the sequence in the same order
        to the internal command storage
        """

        # register the information of the commands
        for cmd in cmds:
            self.register(cmd)

        # and store all the transformed commands
        self.cmds.extend([self.transform(cmd) for cmd in cmds])
