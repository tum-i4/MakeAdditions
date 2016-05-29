import unittest
from makelogic.MakeLlvm import MakeLlvm
from makelogic.config import CLANG, LLVMLINK
from makelogic.constants import EXECFILEEXTENSION


class TestTransformLlvmCCLink(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_cc_link_basic(self):
        self.assertEqual(
            LLVMLINK + " -o divisible" + EXECFILEEXTENSION +
            ".bc main.bc divisible.bc",
            self.llvm.transform("cc -o divisible main.o divisible.o")
        )

    def test_cc_link_with_lib_bzip2(self):
        # At first, we register the library
        self.llvm.register("ar cq libbz2.a blocksort.o huffman.o")
        self.assertTrue("libbz2.a.bc" in self.llvm.libs)

        self.assertEqual(
            LLVMLINK + " -o bzip2" + EXECFILEEXTENSION +
            ".bc bzip2.bc libbz2.a.bc",
            self.llvm.transform(
                "gcc -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 "
                " -o bzip2 bzip2.o -L. -lbz2")
        )

    def test_cc_link_with_lib_flex(self):

        self.llvm.register("ar cru .libs/libcompat.a .libs/lib.o " +
                           ".libs/reallocarray.o")
        self.assertTrue("libcompat.a.bc" in self.llvm.libs)

        self.assertEqual(
            LLVMLINK + " -o stage1flex" + EXECFILEEXTENSION + ".bc scan.bc" +
            " buf.bc ccl.bc dfa.bc ecs.bc filter.bc gen.bc main.bc misc.bc " +
            "nfa.bc options.bc parse.bc regex.bc scanflags.bc scanopt.bc " +
            "skel.bc sym.bc tables.bc tables_shared.bc tblcmp.bc yylex.bc " +
            "../lib/.libs/libcompat.a.bc",
            self.llvm.transform(
                CLANG + " -g -O2 -o stage1flex scan.o buf.o ccl.o dfa.o " +
                "ecs.o filter.o gen.o main.o misc.o nfa.o options.o parse.o " +
                "regex.o scanflags.o scanopt.o skel.o sym.o tables.o " +
                "tables_shared.o tblcmp.o yylex.o " +
                "../lib/.libs/libcompat.a -lm")
        )

    def test_cc_link_shared_flex(self):
        self.assertEqual(
            LLVMLINK + " .libs/libmain.bc .libs/libyywrap.bc " +
            "-o .libs/libfl.so.2.0.0.bc",
            self.llvm.transform(
                CLANG + " -shared -fPIC -DPIC .libs/libmain.o " +
                ".libs/libyywrap.o -lm -g -O2 -Wl,-soname -Wl,libfl.so.2 " +
                "-o .libs/libfl.so.2.0.0")
        )

    def test_cc_link_double_coreutils(self):
        self.llvm.register("ar cr src/libver.a src/version.o")
        self.llvm.register("ar cr lib/libcoreutils.a lib/copy-acl.o")

        self.assertEqual(
            LLVMLINK + " -o src/chroot" + EXECFILEEXTENSION +
            ".bc src/chroot.bc src/libver.a.bc lib/libcoreutils.a.bc",
            self.llvm.transform(
                CLANG + " -g -O2 -Wl,--as-needed -o src/chroot src/chroot.o " +
                "src/libver.a lib/libcoreutils.a lib/libcoreutils.a")
        )
