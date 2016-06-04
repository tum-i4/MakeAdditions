import unittest
from makeadditions.Command import Command
from makeadditions.MakeLlvm import MakeLlvm


class TestTransformLlvm(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_empty(self):
        self.assertEqual(
            Command("", "/tmp"), self.llvm.transform(Command("", "/tmp")))

    def test_failcount(self):
        self.assertEqual(0, self.llvm.skipped)
        self.llvm.transform(
            Command("just impossible to translate wtf", "/tmp"))
        self.assertEqual(1, self.llvm.skipped)
