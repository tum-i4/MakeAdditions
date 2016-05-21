from ..Transformer import TransformerSingle
from ...config import CLANG


class TransformCCCompile(TransformerSingle):

    def canBeAppliedOn(cmd: str) -> bool:
        return any(cmd.startswith(s) for s in ["cc", "gcc"]) and " -c " in cmd

    def applyTransformationOn(cmd: str, container) -> str:
        # tokenize and remove the original command
        tokens = cmd.split()[1:]

        # remove optimizer flags
        tokens = list(filter(lambda t: t not in [
            '-O0', '-O1', '-O2', '-O3', '-Og', '-Os', '-Ofast'], tokens))

        # deactivate optimization
        tokens.insert(0, "-O0")

        # build the new command
        newcmd = CLANG + " -emit-llvm "

        # add -g flag, if it was not there before
        if "-g" not in tokens:
            newcmd += "-g "

        # rename the output-file from .o to .bc, if specified
        if "-o" in tokens:
            pos = tokens.index("-o")
            if tokens[pos + 1].endswith(".o"):
                tokens[pos + 1] = tokens[pos + 1][:-2] + ".bc"

        return newcmd + " ".join(tokens)
