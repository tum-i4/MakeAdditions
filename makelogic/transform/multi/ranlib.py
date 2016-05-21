"""
ranlib - generate index to archive.
"""

from os import linesep
from ..Transformer import TransformerMulti


class TransformRanlib(TransformerMulti):
    """ transform ranlib commands """

    # dirty hack for parsing this commands
    # TODO gather more test data and find a real implementation
    toremove = [
        "if ( test -f ranlib -o -f /usr/bin/ranlib -o \\\n"
        "\t-f /bin/ranlib -o -f /usr/ccs/bin/ranlib ) ; then \\\n"
        "\techo ranlib libbz2.a ; \\\n"
        "\tranlib libbz2.a ; \\\n"
        "fi",
    ]

    @staticmethod
    def can_be_applied_on(cmd: str) -> bool:
        return cmd in TransformRanlib.toremove

    @staticmethod
    def apply_transformation_on(cmd: str, container) -> str:
        return (len(cmd.splitlines()) - 1) * linesep
