"""
Helpfull method to collect a list of all subclasses of a given class
"""

from .Transformer import TransformerLlvm
# Do not remove this wildcard import
# It is needed for automatic transformer registration
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .llvm import *


def list_all_llvm_transformers():
    """
    Get a list of all available transformers for single instruction commands
    """
    return list_all_subclasses(TransformerLlvm)


def list_all_subclasses(superclass):
    """
    Get a list of all subclasses defined for a given superclass
    """

    # sorted for determinism
    return sorted(
        # any class object in python has a meta-function for its subclasses
        [cls for cls in superclass.__subclasses__()],
        # sort based on class name
        key=lambda c: c.__name__
    )
