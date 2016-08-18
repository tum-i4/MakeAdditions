from ..TransformationTestCase import TransformationTestCase
from makeadditions.config import CLANG, LLVMLINK


class TestTransformLlvmCCBoth(TransformationTestCase):

    def test_cc_both_standalone_busybox(self):
        self.assertTransformation(
            CLANG + " -c -emit-llvm -g -O0 -o fixdep.x.bc fixdep.c",
            "gcc -o fixdep fixdep.c"
        )

    def test_cc_compile_and_link_simultaneously_zopfli(self):
        self.assertTransformation(
            CLANG + " -c -emit-llvm -g -O0 blocksplitter.c; " +
            CLANG + " -c -emit-llvm -g -O0 cache.c; " +
            LLVMLINK + " blocksplitter.bc cache.bc -o zopfli.x.bc",
            "gcc blocksplitter.c cache.c -o zopfli"
        )

    def test_cc_both_multifiles_lz4(self):
        self.assertTransformation(
            CLANG + " -c -emit-llvm -g -O0 -I. -std=c99 -Wall "
            "-DXXH_NAMESPACE=LZ4_ lz4.c; " +
            CLANG + " -c -emit-llvm -g -O0 -I. -std=c99 -Wall "
            "-DXXH_NAMESPACE=LZ4_ lz4hc.c; " +
            CLANG + " -c -emit-llvm -g -O0 -I. -std=c99 -Wall "
            "-DXXH_NAMESPACE=LZ4_ lz4frame.c; " +
            CLANG + " -c -emit-llvm -g -O0 -I. -std=c99 -Wall "
            "-DXXH_NAMESPACE=LZ4_ xxhash.c; " +
            LLVMLINK + " lz4.bc lz4hc.bc lz4frame.bc xxhash.bc "
            "-o liblz4.so.1.7.1.bc",
            "cc -O3 -I. -std=c99 -Wall -DXXH_NAMESPACE=LZ4_ "
            "lz4.c lz4hc.c lz4frame.c xxhash.c -o liblz4.so.1.7.1"
        )
