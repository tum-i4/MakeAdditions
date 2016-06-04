"""
cd - change the working directory
"""

from ..Transformer import TransformerLlvm
from ...constants import MAKEANNOTATIONHINT


class TransformCd(TransformerLlvm):
    """ transform cd commands """

    @staticmethod
    def can_be_applied_on(cmd):
        # Keep only makefile cd commands
        return (cmd.bashcmd.startswith("cd ") and
                MAKEANNOTATIONHINT in cmd.annotations)

    @staticmethod
    def apply_transformation_on(cmd, container):
        return cmd
