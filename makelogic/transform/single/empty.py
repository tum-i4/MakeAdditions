from ..Transformer import TransformerSingle


class TransformEmpty(TransformerSingle):

    def canBeAppliedOn(cmd: str) -> bool:
        return not cmd.strip()

    def applyTransformationOn(cmd: str, container) -> str:
        return ""
