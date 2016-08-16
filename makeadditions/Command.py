"""
This container contains a command, that can be executed in a shell, with
some additional informations.
"""

import re
import subprocess


class Command:
    """
    Container class for a shell command
    """

    def __init__(self, bashcmd, curdir, annotations=None):
        self.bashcmd = bashcmd
        self.annotations = annotations or []
        self.curdir = curdir

    def __str__(self):
        # No output for empty commands
        if not self.bashcmd:
            return ""

        return "%s # dir: %s" % (
            self.bashcmd, " ; ".join([self.curdir] + self.annotations))

    def __repr__(self):
        return "%s(%s, %s, %s)" % (
            self.__class__, self.bashcmd, self.curdir, self.annotations)

    def __eq__(self, other):
        return (
            self.bashcmd == other.bashcmd and
            self.annotations == other.annotations and
            self.curdir == other.curdir
        )

    def add_annotation(self, annotation):
        """ Add a annotation to the command """
        self.annotations.append(annotation)

    def is_noop(self):
        """ Checks, if this command perform no operation, e.g. pure
        comment strings or all sorts of empty strings """
        return not self.bashcmd.strip() or self.bashcmd.strip().startswith("#")

    def execute(self):
        """ Execute this program in a shell """

        if re.search(r"\"\S+\"", self.bashcmd):
            self.bashcmd = self.bashcmd.replace('"', '\\"')

        # I know, this shell=True can be evil, but what can we do?
        return subprocess.call(self.bashcmd, shell=True, cwd=self.curdir)

    def is_cd(self):
        """ Checks, if this command is only a cd command """
        return self.bashcmd.startswith("cd ")

    def has_effects(self):
        """ Checks, if this command has actually no effects """
        return not (self.is_noop() or self.is_cd())
