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

    if args.chain == "vanilla":
        print(MakeScript.from_makefile(args.makefile.name, args.target))
    elif args.chain == "klee":
        print(MakeKlee.from_makefile(args.makefile.name, args.target))

if __name__ == "__main__":
    main()
