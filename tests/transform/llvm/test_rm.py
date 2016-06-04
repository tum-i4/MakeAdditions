import unittest
from makeadditions.Command import Command
from makeadditions.MakeLlvm import MakeLlvm
from makeadditions.constants import EXECFILEEXTENSION


class TestTransformLlvmRm(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_rm_single_object_file(self):
        self.assertEqual(
            Command("rm -f main.bc", "/tmp"),
            self.llvm.transform(Command("rm -f main.o", "/tmp")))

    def test_rm_single_static_library(self):
        self.assertEqual(
            Command("rm -f lib.a.bc", "/tmp"),
            self.llvm.transform(Command("rm -f lib.a", "/tmp")))

    def test_rm_single_executable(self):
        self.assertEqual(
            Command("rm -f executable" + EXECFILEEXTENSION + ".bc", "/tmp"),
            self.llvm.transform(Command("rm -f executable", "/tmp")))

    def test_no_rm_for_single_irrelevant(self):
        self.assertEqual(
            Command("", "/tmp"),
            self.llvm.transform(Command("rm -f notrelevant.sh", "/tmp")))

    def test_no_rm_for_two_irrelevant(self):
        self.assertEqual(
            Command("", "/tmp"),
            self.llvm.transform(Command("rm -f one.sh two.sh", "/tmp")))

    def test_rm_wildcard_object(self):
        self.assertEqual(
            Command("rm -f *.bc", "/tmp"),
            self.llvm.transform(Command("rm -f *.o", "/tmp")))

    def test_rm_wildcard_enquoted(self):
        self.assertEqual(
            Command("rm -f *.bc", "/tmp"),
            self.llvm.transform(Command("rm -f '*.o'", "/tmp")))

    def test_rm_mixed_bzip2(self):
        self.assertEqual(
            Command("rm -f *.bc libbz2.a.bc bzip2" + EXECFILEEXTENSION +
                    ".bc bzip2recover" + EXECFILEEXTENSION + ".bc", "/tmp"),
            self.llvm.transform(Command(
                "rm -f '*.o' libbz2.a bzip2 bzip2recover sample1.rb2", "/tmp"))
        )
