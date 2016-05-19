from ..Transformer import Transformer
from ..config import LLVMLINK


class TransformCCLink(Transformer):

    def canBeAppliedOn(cmd: str) -> bool:
        return (any(cmd.startswith(s) for s in ["cc", "gcc"]) and
                " -c " not in cmd)

    def applyTransformationOn(cmd: str, container) -> str:
        # tokenize and remove the original command
        tokens = cmd.split()[1:]

        # remove optimizer flags
        tokens = list(filter(lambda t: t not in ['-O1', '-O2', '-O3'], tokens))

        if "-o" in tokens:
            # append .bc to the output file
            pos = tokens.index("-o")
            tokens[pos + 1] = tokens[pos + 1] + ".x.bc"

        # If we compile against a previos compiled library
        if "-L." in tokens:
            # The local library path is no longer needed
            tokens.remove("-L.")
            tokens[:] = [
                "lib" + t[2:] + ".a.bc"
                if (t.startswith("-l") and
                    "lib" + t[2:] + ".a.bc" in container.libs) else t
                for t in tokens]

        # transform all linked .o-files to the corresponding .bc-file
        tokens = map(
            lambda x: x[:-2] + ".bc" if x.endswith(".o") else x, tokens)

        # filter all command line options except -o
        tokens = filter(lambda t: not t.startswith("-") or t == "-o", tokens)

        return LLVMLINK + " " + " ".join(tokens)
