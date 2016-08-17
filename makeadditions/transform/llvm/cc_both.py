"""
C compiler
"""

from ..Transformer import TransformerLlvm
from ...config import CLANG
from ...constants import (
    COMPILERS,
    DEPENDENCYFLAGS,
    DEPENDENCYEMISSION,
    EXECFILEEXTENSION,
    OPTIMIZERFLAGS
)


class TransformCCBoth(TransformerLlvm):
    """ transform commands, that compile and link at the same time"""

    @staticmethod
    def can_be_applied_on(cmd):
        return (any(cmd.bashcmd.startswith(s + " ") for s in COMPILERS) and
                "-o /dev/null" not in cmd.bashcmd and
                " -c " not in cmd.bashcmd and (
                    ".c " in cmd.bashcmd or cmd.bashcmd.endswith(".c")))

    @staticmethod
    def apply_transformation_on(cmd, container):
        # tokenize and remove the original command
        tokens = cmd.bashcmd.split()[1:]

        # remove optimizer flags
        tokens = [t for t in tokens if t not in OPTIMIZERFLAGS]

        # deactivate optimization
        tokens.insert(0, "-O0")

        # remove dependency emission
        for deptoken in DEPENDENCYEMISSION:
            if deptoken in tokens:
                pos = tokens.index(deptoken)
                del tokens[pos:pos + 2]

        # remove dependency flags
        tokens = [t for t in tokens if t not in DEPENDENCYFLAGS]

        # build the new command
        newcmd = CLANG + " -c -emit-llvm "

        # add -g flag, if it was not there before
        if "-g" not in tokens:
            newcmd += "-g "

        if "-o" in tokens:
            # append .x.bc to the output file
            pos = tokens.index("-o")
            tokens[pos + 1] += EXECFILEEXTENSION + ".bc"

        cmd.bashcmd = newcmd + " ".join(tokens)

        return cmd
