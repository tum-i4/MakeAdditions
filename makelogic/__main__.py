import argparse
import sys
from .MakeScript import MakeScript
from .MakeKlee import MakeKlee


def main():
    """
    Parse some commandline options and start corresponding transformation for
    the given Makefile and target.
    """

    parser = argparse.ArgumentParser(
        description='Convert a Makefile to a sh-script for building with llvm'
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

    args = parser.parse_args()

    if args.target:
        m = MakeScript(args.makefile.name, args.target)
    else:
        m = MakeScript(args.makefile.name)

    klee = MakeKlee()
    for c in m.cmds:
        klee.appendCommand(c)

    print(klee)

    if args is None:
        args = sys.argv[1:]

    print("This is the main routine.")
    print("It should do something interesting.")

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

if __name__ == "__main__":
    main()
