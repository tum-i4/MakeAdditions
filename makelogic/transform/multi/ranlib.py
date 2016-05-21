from ..Transformer import TransformerMulti
from os import linesep


class TransformRanlib(TransformerMulti):

    # dirty hack for parsing this commands
    # TODO gather more test data and find a real implementation
    toremove = [
        "if ( test -f ranlib -o -f /usr/bin/ranlib -o \\\n"
        "\t-f /bin/ranlib -o -f /usr/ccs/bin/ranlib ) ; then \\\n"
        "\techo ranlib libbz2.a ; \\\n"
        "\tranlib libbz2.a ; \\\n"
        "fi",
    ]

    def canBeAppliedOn(cmd: str) -> bool:
        return cmd in TransformRanlib.toremove

    def applyTransformationOn(cmd: str, container) -> str:
        return (len(cmd.splitlines()) - 1) * linesep
