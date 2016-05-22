"""
Common interface for all Transformers. Contains multiple classes as classifier
for identifying the different transformer types.
"""

import abc


class TransformerBase(metaclass=abc.ABCMeta):
    """ Container class for all transformations """

    @staticmethod
    @abc.abstractmethod
    def can_be_applied_on(cmd: str) -> bool:
        """ Check, if this transformation can be applied on cmd """
        return False

    @staticmethod
    @abc.abstractmethod
    def apply_transformation_on(cmd: str, container) -> str:
        """ Apply transformation on cmd """
        return cmd


# pylint: disable=abstract-method
class TransformerLlvm(TransformerBase):
    """ Container class for all llvm transformer"""
    pass
