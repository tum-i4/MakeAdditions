"""
This container contains a command, that can be executed in a shell, with
some additional informations.
"""

import re
import subprocess
from os import path
from .config import LLVMOPT, OPTDELETE


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

        retry = True
        offset = 0
        while retry:
            retry = False
            offset += 1
            try:
                # I know, this shell=True can be evil, but what can we do?
                subprocess.check_output(
                    self.bashcmd, shell=True,
                    stderr=subprocess.STDOUT, cwd=self.curdir)
            except subprocess.CalledProcessError as exc:
                # Try to solve link error with multiple definitions
                linkerr = re.search(
                    "Linking globals named '([^']*)': symbol multiply defined!",
                    exc.output.decode("utf-8"))
                multfunc = linkerr.group(1)

                # This is a nasty hack, feel free to suggest improvements
                candidates = [c for c in self.bashcmd.split()
                              if c.endswith(".bc") and not c.endswith(".x.bc")]

                tbcfile = candidates[-offset]
                splitpoint = len(path.basename(tbcfile))
                newtbcfile = tbcfile[:-splitpoint] + '_' + tbcfile[-splitpoint:]
                if offset == len(candidates):
                    continue

                # Delete the double defined function
                if linkerr and LLVMOPT and OPTDELETE:
                    subprocess.call(
                        [LLVMOPT, "-load", OPTDELETE, "-deletedefinition",
                         tbcfile, "-deletefunction", multfunc,
                         "-o", newtbcfile], cwd=self.curdir)
                    self.bashcmd = self.bashcmd.replace(tbcfile, newtbcfile)

                    retry = True
                else:
                    print(exc.output.decode("utf-8"))
                    return exc.returncode

        return 0

    def is_cd(self):
        """ Checks, if this command is only a cd command """
        return self.bashcmd.startswith("cd ")

    def has_effects(self):
        """ Checks, if this command has actually no effects """
        return not (self.is_noop() or self.is_cd())
