import unittest
from makeadditions.Command import Command
from makeadditions.MakeLlvm import MakeLlvm
from makeadditions.config import CLANG


class TestTransformLlvmCCCompile(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_cc_compile_basic(self):
        self.assertEqual(
            Command(CLANG + " -emit-llvm -g -O0 -c -o main.bc main.c", "/tmp"),
            self.llvm.transform(Command("cc    -c -o main.bc main.c", "/tmp"))
        )

    def test_cc_compile_bzip2(self):
        self.assertEqual(
            Command(CLANG + " -emit-llvm -O0 -Wall -Winline -g "
                    "-D_FILE_OFFSET_BITS=64 -c blocksort.c", "/tmp"),
            self.llvm.transform(
                Command("gcc -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 "
                        "-c blocksort.c", "/tmp"))
        )

    def test_cc_compile_with_userconfig_basic(self):
        self.assertEqual(
            Command(CLANG + " -emit-llvm -g -O0 -c -o main.bc main.c", "/tmp"),
            self.llvm.transform(
                Command(CLANG + "    -c -o main.bc main.c", "/tmp"))
        )

    def test_cc_compile_flags_flex(self):
        self.assertEqual(Command(
            CLANG + " -emit-llvm -O0 -DHAVE_CONFIG_H -I. -I../src -g " +
            "-c lib.c -fPIC -DPIC -o .libs/lib.bc", "/tmp"),
            self.llvm.transform(Command(
                CLANG + " -DHAVE_CONFIG_H -I. -I../src -g " +
                "-O2  -MT lib.lo -MD -MP -MF .deps/lib.Tpo -c lib.c " +
                "-fPIC -DPIC -o .libs/lib.o", "/tmp"))
        )

    def test_cc_compile_localdir_flex(self):
        self.assertEqual(Command(
            CLANG + " -emit-llvm -O0 -DHAVE_CONFIG_H -I. " +
            "'-DLOCALEDIR=" + '"' + "/usr/local/share/locale" + '"' + "'" +
            "-I../intl -g -c libmain.c -fPIC -DPIC -o .libs/libmain.bc",
            "/tmp"),
            self.llvm.transform(Command(
                CLANG + " -DHAVE_CONFIG_H -I. " +
                "'-DLOCALEDIR=" + '"' + "/usr/local/share/locale" + '"' + "'" +
                "-I../intl -g -O2 -MT libmain.lo -MD -MP -MF " +
                ".deps/libmain.Tpo -c libmain.c -fPIC -DPIC " +
                "-o .libs/libmain.o", "/tmp"))
        )
