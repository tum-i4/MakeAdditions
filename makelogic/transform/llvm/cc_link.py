"""
object linker
"""

from ..Transformer import TransformerLlvm
from ...config import LLVMLINK
from ...constants import OPTIMIZERFLAGS, EXECFILEEXTENSION


class TransformCCLink(TransformerLlvm):
    """ transform linker commands """

    @staticmethod
    def can_be_applied_on(cmd: str) -> bool:
        return (any(cmd.startswith(s) for s in ["cc", "gcc"]) and
                " -c " not in cmd)

    @staticmethod
    def apply_transformation_on(cmd: str, container) -> str:
        # tokenize and remove the original command
        tokens = cmd.split()[1:]

        # remove optimizer flags
        tokens = [t for t in tokens if t not in OPTIMIZERFLAGS]

        if "-o" in tokens:
            # append .bc to the output file
            pos = tokens.index("-o")
            tokens[pos + 1] = tokens[pos + 1] + EXECFILEEXTENSION + ".bc"

        # If we compile against a previos compiled library
        if "-L." in tokens:
            # The local library path is no longer needed
            tokens.remove("-L.")

            # replace -l flags, if the library was llvm-compiled earlier
            tokens = [
                "lib" + t[2:] + ".a.bc"
                if (t.startswith("-l") and
                    "lib" + t[2:] + ".a.bc" in container.libs) else t
                for t in tokens]

        # transform all linked .o-files to the corresponding .bc-file
        tokens = [t[:-2] + ".bc" if t.endswith(".o") else t for t in tokens]

        # filter all command line options except -o
        tokens = [t for t in tokens if not t.startswith("-") or t == "-o"]

        return LLVMLINK + " " + " ".join(tokens)
