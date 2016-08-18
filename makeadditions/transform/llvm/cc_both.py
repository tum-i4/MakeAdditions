"""
C compiler
"""

from os import path
from ..Transformer import TransformerLlvm
from ...config import CLANG, LLVMLINK
from ...constants import (
    COMPILERS,
    DEPENDENCYFLAGS,
    DEPENDENCYEMISSION,
    EXECFILEEXTENSION,
    OPTIMIZERFLAGS
)
from ...helper import no_duplicates


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

        # Extract all c files
        cfiles = [f for f in tokens if f.endswith(".c")]

        # remove dependency flags
        tokens = [t for t in tokens if t not in DEPENDENCYFLAGS]

        if (len(cfiles) > 1):
            tokens = [t for t in tokens if not t.endswith(".c")]

            # Build the prepended compile flags
            newcmd = ""
            newtokens = tokens[:]

            if "-o" in newtokens:
                # remove output file
                pos = tokens.index("-o")
                newtokens.pop(pos)
                newtokens.pop(pos)

            for cfile in cfiles:
                newpart = CLANG + " -c -emit-llvm "
                # add -g flag, if it was not there before
                if "-g" not in tokens:
                    newpart += "-g "

                newcmd += (newpart + " ".join(newtokens) + " " + cfile +
                           " -o " + cfile[:-1] + "bc" + "; ")

            # And build the link command
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

            # filter all command line options except -o
            flagstarts = ["-", "'-", '"-']
            tokens = [t for t in tokens if not (
                any(t.startswith(start) for start in flagstarts)) or t == "-o"]

            cmd.bashcmd = (newcmd + LLVMLINK + " " +
                           " ".join([c[:-1] + "bc" for c in cfiles]) + " " +
                           " ".join(no_duplicates(tokens)))
            return cmd

        else:
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
