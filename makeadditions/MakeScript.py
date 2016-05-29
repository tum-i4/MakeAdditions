"""
This class represents and stores the tasks and commands from a
Makefile (and a specific target). It can be printed as an .sh-script
"""

import re
import subprocess
from os import linesep, path
from sys import stderr
from .execute import run_make_with_debug_shell
from .parse import (
    check_debugshell_and_makefile,
    is_noop,
    translate_to_commands
)


class MakeScript:

    """
    The sh-script representation of the tasks from a Makefile
    """

    def __init__(self):
        """ Just init an empty makefile """

        # List for all commands
        self.cmds = []

        # Set of all used libraries
        self.libs = set({})

    def register(self, cmd):
        """ Extract and store informations needed by other commands """

        # look for generated libraries
        if cmd.startswith("ar "):
            libmatch = re.search(r"ar [cruq]+ ([^ ]+\.a)", cmd)
            if libmatch:
                self.libs.add(path.basename(libmatch.group(1)) + ".bc")

    # pylint: disable=no-self-use
    def transform(self, cmd):
        """ Apply transformation to the vanilla command before it is stored """
        return cmd

    @classmethod
    def from_makefile(cls, makefile, targets=None):
        """ Alternative constructor from makefile on the filesystem """
        targets = targets or ["all"]

        # Start with an empty Makescript
        new = cls()

        # Collect the output from make with debug flags
        output = run_make_with_debug_shell(makefile, targets)

        # Check, if the output can be translated properly
        check_debugshell_and_makefile(output)

        # Translate all the commands
        cmds = translate_to_commands(output)

        # store relevant information for later commands
        for cmd in cmds:
            new.register(cmd)

        # and store the translated commands
        new.cmds = [new.transform(cmd) for cmd in cmds]

        return new

    def __str__(self):
        """ Print the stored command as a sh-script """
        return linesep.join(self.cmds)

    def execute_cmds(self, keep_going=False):
        """
        Execute all the transformed commands.
        Hopefully this results in a full llvm-build
        """

        # filter all noop commands
        cmds = (cmd for cmd in self.cmds if not is_noop(cmd))

        # Variables to track directory changes
        curdir = "/dev/null"

        for cmd in cmds:
            if cmd.startswith("cd "):
                # we need a special logic for cd in the subprocesses
                curdir = cmd[3:].split("#")[0].strip()
            else:
                # Other commands are executed in a seperate subprocess

                # I know, this shell=True can be evil, but what can we do?
                code = subprocess.call(cmd, shell=True, cwd=curdir)

                # Stop on the first error
                if code != 0:
                    if keep_going:
                        print("Execution failed for '%s'" % cmd, file=stderr)
                    else:
                        raise OSError("Execution failed for '%s'" % cmd)

    def append_cmd(self, cmd):
        """ Append a command to the internal command storage """

        # register the information of the command
        self.register(cmd)

        # and store the transformed command
        self.cmds.append(self.transform(cmd))

    def append_cmdlist(self, cmds):
        """
        Append all commands from the sequence in the same order
        to the internal command storage
        """

        # register the information of the commands
        for cmd in cmds:
            self.register(cmd)

        # and store all the transformed commands
        self.cmds.extend([self.transform(cmd) for cmd in cmds])
