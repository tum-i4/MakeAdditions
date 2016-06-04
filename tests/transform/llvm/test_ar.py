from ..TransformationTestCase import TransformationTestCase
from makeadditions.config import LLVMLINK


class TestTransformLlvmAr(TransformationTestCase):

    def test_ar_cq_bzip2(self):
        self.assertTransformation(
            LLVMLINK + " -o libbz2.a.bc blocksort.bc huffman.bc",
            "ar cq libbz2.a blocksort.o huffman.o", "/tmp"
        )

    def test_ar_cru_flex(self):
        self.assertTransformation(
            LLVMLINK + " -o .libs/libcompat.a.bc .libs/lib.bc " +
            ".libs/reallocarray.bc",
            "ar cru .libs/libcompat.a .libs/lib.o .libs/reallocarray.o"
        )
