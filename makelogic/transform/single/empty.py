"""
 - just empty strings
"""

from ..Transformer import TransformerSingle


class TransformEmpty(TransformerSingle):
    """ transform empty commands """

    @staticmethod
    def can_be_applied_on(cmd: str) -> bool:
        return not cmd.strip()

    @staticmethod
    def apply_transformation_on(cmd: str, container) -> str:
        return ""
