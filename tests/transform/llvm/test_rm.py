import unittest
from makeadditions.MakeLlvm import MakeLlvm
from makeadditions.constants import EXECFILEEXTENSION


class TestTransformLlvmRm(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_rm_single_object_file(self):
        self.assertEqual(
            "rm -f main.bc",
            self.llvm.transform("rm -f main.o"))

    def test_rm_single_static_library(self):
        self.assertEqual(
            "rm -f lib.a.bc",
            self.llvm.transform("rm -f lib.a"))

    def test_rm_single_executable(self):
        self.assertEqual(
            "rm -f executable" + EXECFILEEXTENSION + ".bc",
            self.llvm.transform("rm -f executable"))

    def test_no_rm_for_single_irrelevant(self):
        self.assertEqual("", self.llvm.transform("rm -f notrelevant.sh"))

    def test_no_rm_for_two_irrelevant(self):
        self.assertEqual("", self.llvm.transform("rm -f one.sh two.sh"))

    def test_rm_wildcard_object(self):
        self.assertEqual("rm -f *.bc", self.llvm.transform("rm -f *.o"))

    def test_rm_wildcard_enquoted(self):
        self.assertEqual("rm -f *.bc", self.llvm.transform("rm -f '*.o'"))

    def test_rm_mixed_bzip2(self):
        self.assertEqual(
            "rm -f *.bc libbz2.a.bc bzip2" + EXECFILEEXTENSION +
            ".bc bzip2recover" + EXECFILEEXTENSION + ".bc",
            self.llvm.transform(
                "rm -f '*.o' libbz2.a bzip2 bzip2recover sample1.rb2")
        )
