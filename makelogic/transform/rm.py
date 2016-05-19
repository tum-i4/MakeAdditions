from ..Transformer import Transformer
import re


class TransformRm(Transformer):

    def canBeAppliedOn(cmd: str) -> bool:
        return cmd.startswith("rm ") and re.search("rm -f \w+.a", cmd)

    def applyTransformationOn(cmd: str, container) -> str:
        return ""
