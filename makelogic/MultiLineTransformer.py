from os import linesep


class MultiLineTransformer(object):

    """
    Dirty hack for parsing multi-line commands
    TODO: gather more input for proper test-cases
    """

    toremove = [
        "if ( test -f ranlib -o -f /usr/bin/ranlib -o \\\n"
        "\t-f /bin/ranlib -o -f /usr/ccs/bin/ranlib ) ; then \\\n"
        "\techo ranlib libbz2.a ; \\\n"
        "\tranlib libbz2.a ; \\\n"
        "fi",
    ]

    @staticmethod
    def canBeAppliedOn(cmd: str) -> bool:
        return cmd in MultiLineTransformer.toremove

    @staticmethod
    def applyTransformationOn(cmd: str, container) -> str:
        return (len(cmd.splitlines()) - 1) * linesep
