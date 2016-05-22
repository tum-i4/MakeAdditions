import unittest
from makelogic.MakeLlvm import MakeLlvm
from makelogic.config import CLANG, LLVMLINK
from makelogic.constants import MAKEANNOTATIONHINT


class TestTransformLlvm(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_empty(self):
        self.assertEqual("", self.llvm.transform(""))

    def test_failcount(self):
        self.assertEqual(0, self.llvm.skipped)
        self.llvm.transform("just impossible to translate wtf")
        self.assertEqual(1, self.llvm.skipped)

    def test_cd(self):
        # remove shell cd-commands
        self.assertEqual("", self.llvm.transform("cd mydir"))
        # but keep cd from make annotations
        self.assertEqual(
            "cd mydir" + MAKEANNOTATIONHINT,
            self.llvm.transform("cd mydir" + MAKEANNOTATIONHINT))

    def test_cc_compile(self):
        self.assertEqual(
            CLANG + " -emit-llvm -g -O0 -c -o main.bc main.c",
            self.llvm.transform("cc    -c -o main.bc main.c")
        )
        self.assertEqual(
            CLANG + " -emit-llvm -O0 -Wall -Winline -g "
                    "-D_FILE_OFFSET_BITS=64 -c blocksort.c",
            self.llvm.transform(
                "gcc -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 "
                "-c blocksort.c")
        )

    def test_cc_link(self):
        self.assertEqual(
            LLVMLINK + " -o divisible.x.bc main.bc divisible.bc",
            self.llvm.transform("cc -o divisible main.o divisible.o")
        )

    def test_cc_link_with_lib(self):
        # At first, we register the library
        self.llvm.register("ar cq libbz2.a blocksort.o huffman.o")

        self.assertEqual(
            LLVMLINK + " -o bzip2.x.bc bzip2.bc libbz2.a.bc",
            self.llvm.transform(
                "gcc -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 "
                " -o bzip2 bzip2.o -L. -lbz2")
        )

    def test_ar(self):
        self.assertEqual(
            LLVMLINK + " -o libbz2.a.bc blocksort.bc huffman.bc",
            self.llvm.transform("ar cq libbz2.a blocksort.o huffman.o")
        )

    def test_rm(self):
        self.assertEqual(
            "rm -f main.o.bc",
            self.llvm.transform("rm -f main.o"))

        self.assertEqual(
            "rm -f lib.a.bc",
            self.llvm.transform("rm -f lib.a"))

        self.assertEqual(
            "rm -f executable.x.bc",
            self.llvm.transform("rm -f executable"))

        self.assertEqual("", self.llvm.transform("rm -f notrelevant.sh"))

        self.assertEqual("rm -f *.o.bc", self.llvm.transform("rm -f *.o"))

        self.assertEqual(
            "rm -f '*.o.bc'",
            self.llvm.transform("rm -f '*.o'"))
