import unittest
from os import linesep
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
            CLANG + " -emit-llvm -Wall -Winline -g "
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
        self.assertEqual(
            LLVMLINK + " -o bzip2.x.bc bzip2.bc libbz2.a.bc",
            self.klee.transformToLLVM(
                "gcc -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 "
                " -o bzip2 bzip2.o -L. -lbz2")
        )

    def test_rm(self):
        self.assertEqual(
            "",
            self.klee.transformToLLVM("rm -f libbz2.a")
        )

    def test_ar(self):
        self.assertEqual(
            LLVMLINK + " -o libbz2.a.bc blocksort.bc huffman.bc",
            self.klee.transformToLLVM("ar cq libbz2.a blocksort.o huffman.o")
        )

    def test_twoLinesTwoCommands(self):
        self.assertEqual(linesep * 4, self.klee.transformToLLVM(
            "if ( test -f ranlib -o -f /usr/bin/ranlib -o \\\n"
            "\t-f /bin/ranlib -o -f /usr/ccs/bin/ranlib ) ; then \\\n"
            "\techo ranlib libbz2.a ; \\\n"
            "\tranlib libbz2.a ; \\\n"
            "fi"))
