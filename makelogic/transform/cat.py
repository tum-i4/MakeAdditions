from ..Transformer import Transformer


class TransformCat(Transformer):

    def canBeAppliedOn(cmd: str) -> bool:
        return cmd.startswith("cat ")

    def applyTransformationOn(cmd: str, container) -> str:
        return ""
