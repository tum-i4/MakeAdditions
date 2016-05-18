from ..Transformer import Transformer


class TransformEmpty(Transformer):

    def canBeAppliedOn(cmd: str) -> bool:
        return not cmd.strip()

    def applyTransformationOn(cmd: str, container) -> str:
        return ""
