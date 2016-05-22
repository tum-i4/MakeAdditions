"""
This script provides the entry point for the main module function.
For a given Makefile (and target) it will transform all actions for the given
toolchain. This actions are executed afterwards.
"""

import argparse
from os import getcwd, path
from sys import stderr
from .MakeScript import MakeScript
from .MakeLlvm import MakeLlvm


def main():
    """
    Parse some commandline options, record and transform the commands, and
    finally perform an llvm build.
    """

    parser = argparse.ArgumentParser(
        description="""\
        Execute a normal make command for the given target and record all
        commands invoked during the build process. This commands are filtered
        and transformed to emit llvm-bytecode for all compiler commands. This
        second build process is executed afterwards.
        """
    )

    parser.add_argument(
        'target',
        nargs="?",
        help='Target for make'
    )
    parser.add_argument(
        '--dry-run',
        dest="dry_run",
        help="Print all generated llvm commands, but do not execute them",
        action="store_true",
    )
    parser.add_argument(
        "--just-record",
        dest="just_record",
        help="Just record all the invoked commands, but do not transform, "
             "filter or execute them in any way. They are printed afterwards",
        action="store_true",
    )

    args = parser.parse_args()
    makefile = path.join(getcwd(), "Makefile")

    if not path.isfile(makefile):
        print("Error: Makefile not found. Tried", makefile, file=stderr)
        return

    if args.just_record:
        # run make and print recorded commands
        print(MakeScript.from_makefile(makefile, args.target))
        return

    # execute make and transform commands
    llvm = MakeLlvm().from_makefile(makefile, args.target)

    if args.dry_run:
        print(llvm)
    else:
        llvm.execute_cmds()

if __name__ == "__main__":
    main()
