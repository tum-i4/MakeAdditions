#!/usr/bin/env python

import argparse
from makelogic.MakeKlee import MakeKlee
from makelogic.MakeScript import MakeScript

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Convert a Makefile to a equivalent sh-script'
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
