"""
ar - create, modify, and extract from archives
"""

import re
from ..Transformer import TransformerLlvm
from ...config import LLVMLINK


class TransformAr(TransformerLlvm):
    """ transform ar commands """

    @staticmethod
    def can_be_applied_on(cmd):
        return cmd.startswith("ar cq ") and re.search(r"ar cq \w+\.a", cmd)

    @staticmethod
    def apply_transformation_on(cmd, container):
        # tokenize and remove the original command with first option
        tokens = cmd.split()[1:]

        # llvm needs a flag for specifying the output file
        tokens[0] = "-o"

        # Add .bc file extension to static archive
        tokens[1] += ".bc"

        # transform all linked .o-files to the corresponding .bc-file
        tokens = [t[:-2] + ".bc" if t.endswith(".o") else t for t in tokens]

        return LLVMLINK + " " + " ".join(tokens)
