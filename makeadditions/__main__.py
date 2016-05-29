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
from .config import check_config


def main():
    """
    Parse some commandline options, record and transform the commands, and
    finally perform an llvm build.
    """

    parser = argparse.ArgumentParser(
        description="""\
        Execute a normal make command for the given target and record all
        commands invoked during the build process. This commands are filtered
        and transformed to emit llvm-bitcode for all compiler commands. These
        commands form a second build process, that is executed afterwards.
        """
    )

    parser.add_argument(
        'target',
        nargs="*",
        default=["all"],
        help='Target for make'
    )
    parser.add_argument(
        '--just-transform',
        dest="just_transform",
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
    parser.add_argument(
        "--keep-going",
        dest="keep_going",
        help="Normally the llvm-build command chain stops, if a single "
             "command fails. With this flag, the error is reported, but all "
             "further commands are executed. Thereby this may report a ton "
             "of errors",
        action="store_true",
    )

    args = parser.parse_args()
    makefile = path.join(getcwd(), "Makefile")

    # Check correct configuration
    check_config()

    if not path.isfile(makefile):
        print("Error: Makefile not found. Tried", makefile, file=stderr)
        return

    if not has_make_something_todo(makefile, args.target):
        print("Nothing to be done for '" + " ".join(args.target) + "'")
        return

    print("Start normal make process for '" + " ".join(args.target) + "' ...")

    if not args.just_record:
        # execute make and transform commands
        llvm = MakeLlvm().from_makefile(makefile, args.target)
        print(" ... done")

        if not args.just_transform:
            # Execute all the captured and transformed commands
            print("Run transformed make commands ...")
            llvm.execute_cmds(args.keep_going)
            print(" ... done")
        else:
            # Output instead of execution for just transform
            print(llvm)

    else:
        # run make and print recorded commands
        plain = MakeScript.from_makefile(makefile, args.target)
        print(" ... done")
        print(plain)


if __name__ == "__main__":
    main()
