from .MultiLineTransformer import MultiLineTransformer
from .Transformer import Transformer
from .transform import *
from os import linesep
from sys import stderr


def listAllTransformers():
    # sorted for determinism
    return sorted(
        [cls for cls in Transformer.__subclasses__()],
        key=lambda c: c.__name__
    )


class MakeKlee:

    """
    The .sh-script representation of the tasks from a Makefile converted to
    the logic of KLEE analysis, i.e. using llvm code
    """

    cmds = []
    libs = set({})
    fails = 0

    def __init__(self):
        pass

    def appendCommand(self, cmd: str):
        self.cmds.append(self.transformToLLVM(cmd))

    def transformToLLVM(self, cmd: str) -> str:
        if any(c in cmd for c in ["&&", "|", ";", ">", "<"]):
            if MultiLineTransformer.canBeAppliedOn(cmd):
                return MultiLineTransformer.applyTransformationOn(cmd, self)
            else:
                self.fails += 1
                return cmd + " # Sorry, no transformation found"

        applicable = list(filter(
            lambda l: l.canBeAppliedOn(cmd),
            listAllTransformers()
        ))

        if not applicable:
            self.fails += 1
            return cmd + " # Sorry, no transformation found"
        elif len(applicable) == 1:
            return applicable[0].applyTransformationOn(cmd, self)
        else:
            print(applicable, file=stderr)
            print(cmd, file=stderr)
            raise Exception("Multiple Transformers match")

    def __str__(self):
        result = "#!/bin/sh" + (linesep * 2) + linesep.join(self.cmds)

        # Append a warning, if there were untransformed commands
        if self.fails > 0:
            result += (
                linesep +
                "# Warning {0} commands were not transformed ({0:.2%})".format(
                    self.fails, self.fails / len(self.cmds)))

        return result
