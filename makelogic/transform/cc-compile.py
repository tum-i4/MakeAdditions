from ..Transformer import Transformer
from ..config import CLANG


class TransformCCCompile(Transformer):

    def canBeAppliedOn(cmd: str) -> bool:
        return any(cmd.startswith(s) for s in ["cc", "gcc"]) and " -c " in cmd

    def applyTransformationOn(cmd: str, container) -> str:
        # tokenize and remove the original command
        tokens = cmd.split()[1:]

        newcmd = CLANG + " -emit-llvm "
        if "-g" not in tokens:
            newcmd += "-g "

        if "-o" in tokens:
            pos = tokens.index("-o")
            if tokens[pos + 1].endswith(".o"):
                tokens[pos + 1] = tokens[pos + 1][:-2] + ".bc"

        return newcmd + " ".join(tokens)
