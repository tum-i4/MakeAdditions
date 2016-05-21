"""
Helpfull method to collect a list of all subclasses of a given class
"""

from .Transformer import TransformerSingle, TransformerMulti
# Do not remove this wildcard imports
# They are needed for automatic transformer registration
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .single import *
from .multi import *


def list_all_single_transformers():
    """
    Get a list of all available transformers for single instruction commands
    """
    return list_all_subclasses(TransformerSingle)


def list_all_multi_transformers():
    """
    Get a list of all available transformers for multi instruction commands
    """
    return list_all_subclasses(TransformerMulti)


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
