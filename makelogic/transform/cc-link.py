from ..Transformer import Transformer
from ..config import LLVMLINK


class TransformCCLink(Transformer):

    def canBeAppliedOn(cmd: str) -> bool:
        return (any(cmd.startswith(s) for s in ["cc", "gcc"]) and
                " -c " not in cmd and " -L." not in cmd)

    def applyTransformationOn(cmd: str, container) -> str:
        # tokenize and remove the original command
        tokens = cmd.split()[1:]

        # remove optimizer flags
        tokens = list(filter(lambda t: t not in ['-O1', '-O2', '-O3'], tokens))

        if "-o" in tokens:
            # append .bc to the output file
            pos = tokens.index("-o")
            tokens[pos + 1] = tokens[pos + 1] + ".x.bc"

        # transform all linked .o-files to the corresponding .bc-file
        tokens = map(
            lambda x: x[:-2] + ".bc" if x.endswith(".o") else x, tokens)

        return LLVMLINK + " " + " ".join(tokens)
