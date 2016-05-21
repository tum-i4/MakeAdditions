"""
cat - concatenate files and print on the standard output
"""

from ..Transformer import TransformerSingle


class TransformCat(TransformerSingle):
    """ transform cat commands """

    @staticmethod
    def can_be_applied_on(cmd: str) -> bool:
        return cmd.startswith("cat ")

    @staticmethod
    def apply_transformation_on(cmd: str, container) -> str:
        return ""
