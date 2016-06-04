import unittest
from makeadditions.Command import Command
from makeadditions.MakeLlvm import MakeLlvm
from makeadditions.config import LLVMLINK


class TestTransformLlvmAr(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_ar_cq_bzip2(self):
        self.assertEqual(Command(
            LLVMLINK + " -o libbz2.a.bc blocksort.bc huffman.bc", "/tmp"),
            self.llvm.transform(
                Command("ar cq libbz2.a blocksort.o huffman.o", "/tmp"))
        )

    def test_ar_cru_flex(self):
        self.assertEqual(Command(
            LLVMLINK + " -o .libs/libcompat.a.bc .libs/lib.bc " +
            ".libs/reallocarray.bc", "/tmp"),
            self.llvm.transform(
                Command("ar cru .libs/libcompat.a .libs/lib.o " +
                        ".libs/reallocarray.o", "/tmp"))
        )
