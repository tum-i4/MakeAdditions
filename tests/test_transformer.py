import unittest
from textwrap import dedent
from makelogic.MakeKlee import MakeKlee
from makelogic.config import CLANG, LLVMLINK


class TestPaserSplitInCommands(unittest.TestCase):

    def setUp(self):
        self.klee = MakeKlee()

    def test_empty(self):
        self.assertEqual("", self.klee.transformToLLVM(""))

    def test_cd(self):
        self.assertEqual("cd mydir", self.klee.transformToLLVM("cd mydir"))

    def test_cat(self):
        self.assertEqual("", self.klee.transformToLLVM("cat dummyfile"))
        # TODO stronger assert
        self.assertNotEqual(
            "", self.klee.transformToLLVM("cat dummyfile > target"))

    def test_cc_compile(self):
        self.assertEqual(
            CLANG + " -emit-llvm -g -c -o main.bc main.c",
            self.klee.transformToLLVM("cc    -c -o main.bc main.c")
        )
        self.assertEqual(
            CLANG + " -emit-llvm -Wall -Winline -O2 -g "
                    "-D_FILE_OFFSET_BITS=64 -c blocksort.c",
            self.klee.transformToLLVM(
                "gcc -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 "
                "-c blocksort.c")
        )

    def test_cc_link(self):
        self.assertEqual(
            LLVMLINK + " -o divisible.x.bc main.bc divisible.bc",
            self.klee.transformToLLVM("cc -o divisible main.o divisible.o")
        )

    @unittest.skip("Not yet implemented")
    def test_twoLinesTwoCommands(self):
        self.assertEqual("", self.klee.transformToLLVM(dedent(
            """\
            if ( test -f ranlib -o -f /usr/bin/ranlib -o \
            \t-f /bin/ranlib -o -f /usr/ccs/bin/ranlib ) ; then \
            \techo ranlib libbz2.a ; \
            \tranlib libbz2.a ; \
            fi
            """)))
