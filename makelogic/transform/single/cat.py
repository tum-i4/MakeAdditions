from ..Transformer import TransformerSingle


class TransformCat(TransformerSingle):

    def canBeAppliedOn(cmd: str) -> bool:
        return cmd.startswith("cat ")

    def applyTransformationOn(cmd: str, container) -> str:
        return ""
