import unittest
from makelogic.MakeLlvm import MakeLlvm
from makelogic.config import LLVMLINK


class TestTransformLlvmAr(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_ar_cq_bzip2(self):
        self.assertEqual(
            LLVMLINK + " -o libbz2.a.bc blocksort.bc huffman.bc",
            self.llvm.transform("ar cq libbz2.a blocksort.o huffman.o")
        )

    def test_ar_cru_flex(self):
        self.assertEqual(
            LLVMLINK + " -o .libs/libcompat.a.bc .libs/lib.bc " +
            ".libs/reallocarray.bc",
            self.llvm.transform("ar cru .libs/libcompat.a .libs/lib.o " +
                                ".libs/reallocarray.o")
        )
