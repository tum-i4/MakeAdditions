import unittest
from makeadditions.execute import check_clang, check_llvmlink


class TestCheckClang(unittest.TestCase):

    def test_wrong_clang(self):
        self.assertRaises(Exception, check_clang, "idonotexist")


class TestCheckLlvmlink(unittest.TestCase):

    def test_wrong_llvmlink(self):
        self.assertRaises(Exception, check_llvmlink, "idonotexist")
