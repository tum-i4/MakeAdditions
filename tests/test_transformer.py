import unittest
from os import linesep
from makelogic.MakeKlee import MakeKlee
from makelogic.config import CLANG, LLVMLINK


class TestPaserSplitInCommands(unittest.TestCase):

    def setUp(self):
        self.klee = MakeKlee()

    def test_empty(self):
        self.assertEqual("", self.klee.transform(""))

    def test_failcount(self):
        self.assertEqual(0, self.klee.fails)
        self.klee.transform("impossible to translate wtf")
        self.assertEqual(1, self.klee.fails)

    def test_cd(self):
        self.assertEqual("cd mydir", self.klee.transform("cd mydir"))

    def test_cat(self):
        self.assertEqual("", self.klee.transform("cat dummyfile"))
        self.assertNotEqual("", self.klee.transform("cat dummyfile > target"))

    def test_cc_compile(self):
        self.assertEqual(
            CLANG + " -emit-llvm -g -O0 -c -o main.bc main.c",
            self.klee.transform("cc    -c -o main.bc main.c")
        )
        self.assertEqual(
            CLANG + " -emit-llvm -O0 -Wall -Winline -g "
                    "-D_FILE_OFFSET_BITS=64 -c blocksort.c",
            self.klee.transform(
                "gcc -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 "
                "-c blocksort.c")
        )

    def test_cc_link(self):
        self.assertEqual(
            LLVMLINK + " -o divisible.x.bc main.bc divisible.bc",
            self.klee.transform("cc -o divisible main.o divisible.o")
        )

    def test_cc_link_with_lib(self):
        # At first, we register the library
        self.klee.register("ar cq libbz2.a blocksort.o huffman.o")

        self.assertEqual(
            LLVMLINK + " -o bzip2.x.bc bzip2.bc libbz2.a.bc",
            self.klee.transform(
                "gcc -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 "
                " -o bzip2 bzip2.o -L. -lbz2")
        )

    def test_rm(self):
        self.assertEqual(
            "",
            self.klee.transform("rm -f libbz2.a")
        )

    def test_ar(self):
        self.assertEqual(
            LLVMLINK + " -o libbz2.a.bc blocksort.bc huffman.bc",
            self.klee.transform("ar cq libbz2.a blocksort.o huffman.o")
        )

    def test_twoLinesTwoCommands(self):
        self.assertEqual(linesep * 4, self.klee.transform(
            "if ( test -f ranlib -o -f /usr/bin/ranlib -o \\\n"
            "\t-f /bin/ranlib -o -f /usr/ccs/bin/ranlib ) ; then \\\n"
            "\techo ranlib libbz2.a ; \\\n"
            "\tranlib libbz2.a ; \\\n"
            "fi"))
