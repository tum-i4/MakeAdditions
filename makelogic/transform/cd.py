from ..Transformer import Transformer


class TransformCd(Transformer):

    def canBeAppliedOn(cmd: str) -> bool:
        return cmd.startswith("cd ")

    def applyTransformationOn(cmd: str, container) -> str:
        return cmd
