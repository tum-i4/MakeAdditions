import unittest
from makeadditions.MakeLlvm import MakeLlvm
from makeadditions.constants import MAKEANNOTATIONHINT


class TestTransformLlvmCd(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def test_cd_remove_shell(self):
        self.assertEqual("", self.llvm.transform("cd mydir"))

    def test_cd_keep_make(self):
        self.assertEqual(
            "cd mydir" + MAKEANNOTATIONHINT,
            self.llvm.transform("cd mydir" + MAKEANNOTATIONHINT))
