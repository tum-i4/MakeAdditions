import unittest
from makelogic.MakeLlvm import MakeLlvm
from makelogic.config import CLANG, LLVMLINK
from makelogic.constants import EXECFILEEXTENSION, MAKEANNOTATIONHINT


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
        self.assertEqual(
            CLANG + " -emit-llvm -g -O0 -c -o main.bc main.c",
            self.llvm.transform(CLANG + "    -c -o main.bc main.c")
        )
        self.assertEqual(
            CLANG + " -emit-llvm -O0 -DHAVE_CONFIG_H -I. -I../src -g " +
            "-c lib.c -fPIC -DPIC -o .libs/lib.bc",
            self.llvm.transform(
                CLANG + " -DHAVE_CONFIG_H -I. -I../src -g " +
                "-O2  -MT lib.lo -MD -MP -MF .deps/lib.Tpo -c lib.c " +
                "-fPIC -DPIC -o .libs/lib.o")
        )
        self.assertEqual(
            CLANG + " -emit-llvm -O0 -DHAVE_CONFIG_H -I. " +
            "'-DLOCALEDIR=" + '"' + "/usr/local/share/locale" + '"' + "'" +
            "-I../intl -g -c libmain.c -fPIC -DPIC -o .libs/libmain.bc",
            self.llvm.transform(
                CLANG + " -DHAVE_CONFIG_H -I. " +
                "'-DLOCALEDIR=" + '"' + "/usr/local/share/locale" + '"' + "'" +
                "-I../intl -g -O2 -MT libmain.lo -MD -MP -MF " +
                ".deps/libmain.Tpo -c libmain.c -fPIC -DPIC -o .libs/libmain.o"
            )
        )

    def test_cc_link(self):
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

    def test_ar(self):
        self.assertEqual(
            LLVMLINK + " -o libbz2.a.bc blocksort.bc huffman.bc",
            self.llvm.transform("ar cq libbz2.a blocksort.o huffman.o")
        )
        self.assertEqual(
            LLVMLINK + " -o .libs/libcompat.a.bc .libs/lib.bc " +
            ".libs/reallocarray.bc",
            self.llvm.transform("ar cru .libs/libcompat.a .libs/lib.o " +
                                ".libs/reallocarray.o")
        )

    def test_rm(self):
        self.assertEqual(
            "rm -f main.bc",
            self.llvm.transform("rm -f main.o"))

        self.assertEqual(
            "rm -f lib.a.bc",
            self.llvm.transform("rm -f lib.a"))

        self.assertEqual(
            "rm -f executable" + EXECFILEEXTENSION + ".bc",
            self.llvm.transform("rm -f executable"))

        self.assertEqual("", self.llvm.transform("rm -f notrelevant.sh"))

        self.assertEqual("rm -f *.bc", self.llvm.transform("rm -f *.o"))

        self.assertEqual(
            "rm -f '*.bc'",
            self.llvm.transform("rm -f '*.o'"))

        self.assertEqual(
            "rm -f '*.bc' libbz2.a.bc bzip2" + EXECFILEEXTENSION +
            ".bc bzip2recover" + EXECFILEEXTENSION + ".bc",
            self.llvm.transform(
                "rm -f '*.o' libbz2.a bzip2 bzip2recover sample1.rb2")
        )
