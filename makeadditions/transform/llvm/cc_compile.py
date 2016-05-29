"""
C compiler
"""

from ..Transformer import TransformerLlvm
from ...config import CLANG
from ...constants import (
    COMPILERS,
    DEPENDENCYFLAGS,
    DEPENDENCYEMISSION,
    OPTIMIZERFLAGS
)


class TransformCCCompile(TransformerLlvm):
    """ transform compile commands """

    @staticmethod
    def can_be_applied_on(cmd):
        return (
            any(cmd.startswith(s + " ") for s in COMPILERS) and " -c " in cmd)

    @staticmethod
    def apply_transformation_on(cmd, container):
        # tokenize and remove the original command
        tokens = cmd.split()[1:]

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
        newcmd = CLANG + " -emit-llvm "

        # add -g flag, if it was not there before
        if "-g" not in tokens:
            newcmd += "-g "

        # rename the output-file from .o to .bc, if specified
        if "-o" in tokens:
            pos = tokens.index("-o")
            if tokens[pos + 1].endswith(".o"):
                tokens[pos + 1] = tokens[pos + 1][:-2] + ".bc"

        return newcmd + " ".join(tokens)
