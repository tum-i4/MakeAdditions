from ..TransformationTestCase import TransformationTestCase
from makeadditions.config import CLANG


class TestTransformLlvmCCBoth(TransformationTestCase):

    def test_cc_both_standalone_busybox(self):
        self.assertTransformation(
            CLANG + " -c -emit-llvm -g -O0 -o fixdep.x.bc fixdep.c",
            "gcc -o fixdep fixdep.c"
        )

    """
    # TODO think about, what transformation is suitable
    def test_cc_compile_and_link_simultaneously_zopfli(self):
        self.assertTransformation(
            CLANG + " TODO ",
            "gcc blocksplitter.c cache.c -o zopfli"
        )
    """
