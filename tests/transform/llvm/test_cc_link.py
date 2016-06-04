from ..TransformationTestCase import TransformationTestCase
from makeadditions.Command import Command
from makeadditions.config import CLANG, LLVMLINK
from makeadditions.constants import EXECFILEEXTENSION


class TestTransformLlvmCCLink(TransformationTestCase):

    def register(self, cmd, curdir):
        self.llvm.register(Command(cmd, curdir))

    def test_cc_link_basic(self):
        self.assertTransformation(
            LLVMLINK + " -o divisible" + EXECFILEEXTENSION +
            ".bc main.bc divisible.bc",
            "cc -o divisible main.o divisible.o"
        )

    def test_cc_link_with_lib_bzip2(self):
        # At first, we register the library
        self.register("ar cq libbz2.a blocksort.o huffman.o", "/tmp")
        self.assertTrue("libbz2" in self.llvm.libs)

        self.assertTransformation(
            LLVMLINK + " -o bzip2" + EXECFILEEXTENSION +
            ".bc bzip2.bc /tmp/libbz2.a.bc",
            "gcc -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 "
            " -o bzip2 bzip2.o -L. -lbz2",
            "/tmp"
        )

    def test_cc_link_with_lib_flex(self):
        self.register(
            "ar cru .libs/libcompat.a .libs/lib.o .libs/reallocarray.o",
            "/tmp/lib")
        self.assertTrue("libcompat" in self.llvm.libs)

        self.assertTransformation(
            LLVMLINK + " -o stage1flex" + EXECFILEEXTENSION + ".bc scan.bc" +
            " buf.bc ccl.bc dfa.bc ecs.bc filter.bc gen.bc main.bc misc.bc " +
            "nfa.bc options.bc parse.bc regex.bc scanflags.bc scanopt.bc " +
            "skel.bc sym.bc tables.bc tables_shared.bc tblcmp.bc yylex.bc " +
            "/tmp/lib/.libs/libcompat.a.bc",
            CLANG + " -g -O2 -o stage1flex scan.o buf.o ccl.o dfa.o " +
            "ecs.o filter.o gen.o main.o misc.o nfa.o options.o parse.o " +
            "regex.o scanflags.o scanopt.o skel.o sym.o tables.o " +
            "tables_shared.o tblcmp.o yylex.o " +
            "../lib/.libs/libcompat.a -lm",
            "/tmp/src"
        )

    def test_cc_link_shared_flex(self):
        self.assertTransformation(
            LLVMLINK + " .libs/libmain.bc .libs/libyywrap.bc " +
            "-o .libs/libfl.so.2.0.0.bc",
            CLANG + " -shared -fPIC -DPIC .libs/libmain.o " +
            ".libs/libyywrap.o -lm -g -O2 -Wl,-soname -Wl,libfl.so.2 " +
            "-o .libs/libfl.so.2.0.0"
        )

    def test_cc_link_double_coreutils(self):
        self.register("ar cr src/libver.a src/version.o", "/tmp")
        self.register("ar cr lib/libcoreutils.a lib/copy-acl.o", "/tmp")

        self.assertTransformation(
            LLVMLINK + " -o src/chroot" + EXECFILEEXTENSION +
            ".bc src/chroot.bc /tmp/src/libver.a.bc " +
            "/tmp/lib/libcoreutils.a.bc",
            CLANG + " -g -O2 -Wl,--as-needed -o src/chroot src/chroot.o " +
            "src/libver.a lib/libcoreutils.a lib/libcoreutils.a",
            "/tmp"
        )

    def test_cc_link_ngircd(self):
        self.register("ar cru libngportab.a strdup.o", "/tmp/src/portab")
        self.assertTrue("libngportab" in self.llvm.libs)

        self.register("ar cru libngtool.a tool.o", "/tmp/src/tool")
        self.assertTrue("libngtool" in self.llvm.libs)

        self.register("ar cru libngipaddr.a ng_ipaddr.o", "/tmp/src/ipaddr")
        self.assertTrue("libngipaddr" in self.llvm.libs)

        self.assertTransformation(
            LLVMLINK + " -o ngircd.x.bc ngircd.bc array.bc channel.bc " +
            "class.bc client.bc client-cap.bc conf.bc conn.bc " +
            "/tmp/src/portab/libngportab.a.bc /tmp/src/tool/libngtool.a.bc " +
            "/tmp/src/ipaddr/libngipaddr.a.bc",
            CLANG + " -g -O2 -pipe -W -Wall -Wpointer-arith " +
            "-Wstrict-prototypes -fstack-protector '-DSYSCONFDIR=" + '"' +
            "/usr/local/etc" + '"' + "' '-DDOCDIR=" + '"' +
            "/usr/local/share/doc/ngircd" + '"' + "' -L../portab " +
            "-L../tool -L../ipaddr -o ngircd ngircd.o array.o channel.o " +
            "class.o client.o client-cap.o conf.o conn.o " +
            "-lngportab -lngtool -lngipaddr -lz",
            "/tmp"
        )
