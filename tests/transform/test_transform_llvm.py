import unittest
from makeadditions.MakeLlvm import MakeLlvm


class TestTransformLlvm(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_empty(self):
        self.assertEqual("", self.llvm.transform(""))

    def test_failcount(self):
        self.assertEqual(0, self.llvm.skipped)
        self.llvm.transform("just impossible to translate wtf")
        self.assertEqual(1, self.llvm.skipped)
