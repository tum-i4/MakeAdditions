"""
cd - change the working directory
"""

from ..Transformer import TransformerSingle


class TransformCd(TransformerSingle):
    """ transform cd commands """

    @staticmethod
    def can_be_applied_on(cmd: str) -> bool:
        return cmd.startswith("cd ")

    @staticmethod
    def apply_transformation_on(cmd: str, container) -> str:
        return cmd
