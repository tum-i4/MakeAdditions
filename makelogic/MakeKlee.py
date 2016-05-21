from .transform import directory
from .MakeScript import MakeScript
from .parse import is_multicommand
from os import linesep
from sys import stderr


class MakeKlee(MakeScript):

    """
    The .sh-script representation of the tasks from a Makefile converted to
    the logic of KLEE analysis, i.e. using llvm code
    """

    __NOTRANSFORMATIONCOMMENT = " # Sorry, no transformation found"

    def __init__(self):
        super(MakeKlee, self).__init__()

        # Counter for failed transformations
        self.fails = 0

    def transform(self, cmd: str):
        # get all relevant transformations
        if is_multicommand(cmd):
            relevant = directory.list_all_multi_transformers()
        else:
            relevant = directory.list_all_single_transformers()

        # filter for applicable transformations
        applicable = list(filter(lambda l: l.canBeAppliedOn(cmd), relevant))

        if not applicable:
            # if no transformation is applicable, mark this error
            self.fails += 1
            return cmd + self.__NOTRANSFORMATIONCOMMENT
        elif len(applicable) == 1:
            # if exact one transformation is applicable, apply it
            return applicable[0].applyTransformationOn(cmd, self)
        else:
            # if more than one transformation is applicable, the result is
            # ambiguous, so just report this error with some details
            print(applicable, file=stderr)
            print(cmd, file=stderr)
            raise Exception("Multiple Transformers match")

    def __str__(self):
        result = super(MakeKlee, self).__str__()

        # Append a warning, if there were untransformed commands
        if self.fails > 0:
            result += (
                linesep +
                "# Warning {0} commands were not transformed ({0:.2%})".format(
                    self.fails, self.fails / len(self.cmds)))

        return result
