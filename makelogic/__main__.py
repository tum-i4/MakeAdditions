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
from .execute import has_make_something_todo


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
        default="all",
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

    if not has_make_something_todo(makefile, args.target):
        print("Nothing to be done for '" + args.target + "'")
        return

    if not args.just_record:
        # execute make and transform commands
        llvm = MakeLlvm().from_makefile(makefile, args.target)

        if not args.dry_run:
            # Execute all the captured and transformed commands
            llvm.execute_cmds()
        else:
            # Output instead of execution for dry runs
            print(llvm)

    else:
        # run make and print recorded commands
        print(MakeScript.from_makefile(makefile, args.target))


if __name__ == "__main__":
    main()
