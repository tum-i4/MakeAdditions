import argparse
from .MakeScript import MakeScript
from .MakeKlee import MakeKlee


def main():
    """
    Parse some commandline options and start corresponding transformation for
    the given Makefile and target.
    """

    parser = argparse.ArgumentParser(
        description="""\
        Record all actions from a Makefile target to an .sh-Script.
        The commands in this script can be transformed for a different
        compiler-chain (e.g. LLVM).
        """
    )

    parser.add_argument(
        'makefile',
        help="Path and name of the Makefile",
        type=argparse.FileType('r')
    )
    parser.add_argument(
        'target',
        nargs="?",
        help='Target for make'
    )
    parser.add_argument(
        "--chain",
        choices=["klee", "vanilla"],
        default="klee",
        help="Transform all commands in the script for a specific tool chain"
    )

    args = parser.parse_args()

    # For all cases we need to parse the vanilla Makefile
    m = MakeScript(args.makefile.name, args.target)

    if args.chain == "vanilla":
        # No changes needed for vanilla
        print(m)
    elif args.chain == "klee":
        # Transform commands for KLEE
        # TODO find a better interface
        klee = MakeKlee()
        for c in m.cmds:
            klee.appendCommand(c)

        print(klee)

if __name__ == "__main__":
    main()
