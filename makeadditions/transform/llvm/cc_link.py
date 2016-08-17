"""
object linker
"""

from os import path
from ..Transformer import TransformerLlvm
from ...config import LLVMLINK
from ...constants import OPTIMIZERFLAGS, EXECFILEEXTENSION, COMPILERS
from ...helper import no_duplicates


class TransformCCLink(TransformerLlvm):
    """ transform linker commands """

    @staticmethod
    def can_be_applied_on(cmd):
        return (
            any(cmd.bashcmd.startswith(s + " ") for s in COMPILERS) and
            " -c " not in cmd.bashcmd and
            "-o /dev/null" not in cmd.bashcmd and
            ".c " not in cmd.bashcmd and not cmd.bashcmd.endswith(".c"))

    @staticmethod
    def apply_transformation_on(cmd, container):
        # tokenize and remove the original command
        tokens = cmd.bashcmd.split()[1:]

        # remove optimizer flags
        tokens = [t for t in tokens if t not in OPTIMIZERFLAGS]

        if "-o" in tokens:
            # append .bc to the output file
            pos = tokens.index("-o")
            # add marker for executable files e.i. files that are not .so
            if ".so" not in tokens[pos + 1]:
                tokens[pos + 1] += EXECFILEEXTENSION
            tokens[pos + 1] += ".bc"

        # replace -l flags, if the library was llvm-compiled earlier
        tokens = [
            container.libs.get("lib" + t[2:], t)
            if t.startswith("-l") else t
            for t in tokens]

        # replace references to static libraries
        tokens = [
            container.libs.get(path.basename(t[:-2]), t)
            if t.endswith(".a") else t
            for t in tokens]

        # transform all linked .o-files to the corresponding .bc-file
        tokens = [t[:-2] + ".bc" if t.endswith(".o") else t for t in tokens]

        # filter all command line options except -o
        flagstarts = ["-", "'-", '"-']
        tokens = [t for t in tokens if not (
            any(t.startswith(start) for start in flagstarts)) or t == "-o"]

        cmd.bashcmd = LLVMLINK + " " + " ".join(no_duplicates(tokens))
        return cmd
