import unittest
from makeadditions.Command import Command
from makeadditions.MakeLlvm import MakeLlvm
from makeadditions.constants import MAKEANNOTATIONHINT


class TestTransformLlvmCd(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_cd_remove_shell(self):
        self.assertEqual(
            Command("", "/tmp"),
            self.llvm.transform(Command("cd mydir", "/tmp")))

    def test_cd_keep_make(self):
        self.assertEqual(
            Command("cd mydir", "/tmp", [MAKEANNOTATIONHINT]),
            self.llvm.transform(Command(
                "cd mydir", "/tmp", [MAKEANNOTATIONHINT]))
        )
