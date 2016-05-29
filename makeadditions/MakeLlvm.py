"""
This class represents and stores the tasks and commands from a
Makefile (and a specific target), that are transform for a LLVM build.
It can be printed as an .sh-script.
"""

from os import linesep
from sys import stderr
from .transform import directory
from .MakeScript import MakeScript


class MakeLlvm(MakeScript):

    """
    The .sh-script representation of the commands from a Makefile target
    converted to the logic for generating llvm-bitcode
    """

    __NOTRANSFORMATIONCOMMENT = " # Sorry, no transformation found"

    def __init__(self):
        super(MakeLlvm, self).__init__()

        # Counter for failed transformations
        self.skipped = 0

    def transform(self, cmd):
        # get all relevant transformations
        relevant = directory.list_all_llvm_transformers()

        # filter for applicable transformations
        applicable = [transformer for transformer in relevant
                      if transformer.can_be_applied_on(cmd)]

        if not applicable:
            # if no transformation is applicable, skip this command
            self.skipped += 1
            return ""
        elif len(applicable) == 1:
            # if exact one transformation is applicable, apply it
            return applicable[0].apply_transformation_on(cmd, self)
        else:
            # if more than one transformation is applicable, the result is
            # ambiguous, so just report this error with some details
            print(applicable, file=stderr)
            print(cmd, file=stderr)
            raise Exception("Multiple Transformers match")

    def __str__(self):
        result = super(MakeLlvm, self).__str__()

        # Append a warning, if there were untransformed commands
        if self.skipped > 0:
            result += (
                linesep +
                "# Info: {0} commands were skipped ({1:.2%})".format(
                    self.skipped, self.skipped / len(self.cmds)))

        return result
