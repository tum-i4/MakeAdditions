from ..Transformer import TransformerSingle


class TransformCd(TransformerSingle):

    def canBeAppliedOn(cmd: str) -> bool:
        return cmd.startswith("cd ")

    def applyTransformationOn(cmd: str, container) -> str:
        return cmd
