"""
Helpful functions for string and command parsing
"""

import os
import re
from .constants import MAKEANNOTATIONHINT
from .Command import Command


class MakefileDirstack():
    """
    Helper class for transforming the entering and leaving directory
    annotations of make output to corresponding cd commands
    """

    def __init__(self):
        # Stack is needed to define, where we are after leaving
        self.dirstack = [os.getcwd()]

    @staticmethod
    def cd_command_to(directory):
        """ Generate a cd command to the given directory """
        return "cd " + directory + " # " + MAKEANNOTATIONHINT

    def push_dir(self, directory):
        """ Pushes a directory to the stack and return the
        corresponding entering cd command """
        self.dirstack.append(directory)
        return MakefileDirstack.cd_command_to(directory)

    def pop_dir(self, directory):
        """ Pops a directory from the stack and return a cd command to the
        upper directory. Asserts, that directory was on top of the stack """
        check = self.dirstack.pop()
        assert check == directory
        return MakefileDirstack.cd_command_to(self.dirstack[-1])

    def translate_if_dirannotation(self, cmd):
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
                return self.push_dir(match.group('dir'))

            elif match.group('action') == 'Leaving':
                return self.pop_dir(match.group('dir'))

        # return other commands unmodified
        return cmd

    def __str__(self):
        return self.dirstack.__str__()


def extract_debugshell(makeoutput):
    """ Extract all command invocations from shell debug statements and
    make them to normal commands """
    return [line.lstrip("+ ") for line in makeoutput]


def get_relevant_lines(makeoutput):
    """ Remove everything from make output, that is not a makefile annotation
    and shell debug output, but leaves the + sign in front of them """
    return [line for line in makeoutput.splitlines()
            if line.startswith("make") or line.startswith("+")]


def translate_to_commands(makeoutput):
    """ Translate all the output from make, debug-shell and output of commands
    during make, and translate them to executable commands """

    return encapsulate_commands(
        extract_debugshell(
            translate_makeannotations(
                get_relevant_lines(makeoutput))))


def check_debugshell_and_makefile(makeoutput):
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


def translate_makeannotations(makeoutput):
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


def encapsulate_commands(cmdlist):
    """ Encapsulate a list of command strings inside the command class.
    All necessary information is extracted meanwhile. """

    # Empty lists results in empty lists
    if not cmdlist:
        return []

    # Make outputs must start with directory information
    assert is_make_cd_cmd(cmdlist[0])

    # initialize the current dir
    curdir = extract_dir_from_makecd(cmdlist[0])

    result = []
    for cmdstr in cmdlist:

        # separate command from comment
        if "#" in cmdstr:
            cmd, comment = cmdstr.split("#")
        else:
            cmd, comment = cmdstr, None

        # Create the new command object
        cmdobj = Command(cmd.strip(), curdir)

        # add comment as an annotation
        if comment is not None:
            cmdobj.add_annotation(comment.strip())

        result.append(cmdobj)

        # store the cd for the next command, if necessary
        if is_make_cd_cmd(cmdstr):
            curdir = extract_dir_from_makecd(cmdstr)

    return result


def extract_dir_from_makecd(cmd):
    """ Extract the directory from a translated cd of makeoutput """
    assert is_make_cd_cmd(cmd)
    return cmd[3:-len(" # " + MAKEANNOTATIONHINT)]


def is_make_cd_cmd(cmd):
    """ Checks, if the given command is a translated make directory change """
    return cmd.startswith("cd ") and cmd.endswith(" # " + MAKEANNOTATIONHINT)
