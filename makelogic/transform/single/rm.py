"""
rm - remove files or directories
"""

import re
from ..Transformer import TransformerSingle


class TransformRm(TransformerSingle):
    """ transform rm commands """

    @staticmethod
    def can_be_applied_on(cmd: str) -> bool:
        return cmd.startswith("rm ") and re.search(r"rm -f \w+\.a", cmd)

    @staticmethod
    def apply_transformation_on(cmd: str, container) -> str:
        return ""
