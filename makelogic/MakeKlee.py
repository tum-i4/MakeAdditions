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
    fails = 0

    def __init__(self):
        pass

    def appendCommand(self, cmd: str):
        self.cmds.append(self.transformToLLVM(cmd))

    def transformToLLVM(self, cmd: str) -> str:
        if any(c in cmd for c in ["&&", "|", ";", ">", "<"]):
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
        return (
            "#!/bin/sh" + (linesep * 2) + linesep.join(self.cmds) +
            linesep + "# {0} commands not transformed".format(self.fails) +
            " ( {0:.2%} )".format(self.fails / len(self.cmds))
        )
