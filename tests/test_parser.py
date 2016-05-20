import unittest
from textwrap import dedent
from makelogic.parse import *


class TestPaserSplitInCommands(unittest.TestCase):

    def test_empty(self):
        self.assertEqual([], splitInCommands(""))

    def test_singleLine(self):
        self.assertEqual(["gcc -v"], splitInCommands("gcc -v"))

    def test_twoLinesTwoCommands(self):
        self.assertEqual(["cmd1", "cmd2"], splitInCommands(dedent(
            """\
            cmd1
            cmd2
            """)))

    def test_twoLinesOneCommands(self):
        self.assertEqual([dedent("""\
            line 1 \\
                -line 2""")], splitInCommands(dedent("""\
            line 1 \\
                -line 2
            """)))

    def test_threeLinesTwoCommands(self):
        self.assertEqual(["cmd1", dedent("""\
            line 1 \\
                -line 2""")], splitInCommands(dedent("""\
            cmd1
            line 1 \\
                -line 2
            """)))


class TestTranslateMakeAnnotations(unittest.TestCase):

    def test_empty(self):
        self.assertRaises(Exception, translateMakeAnnotations, [])

    def test_noDirectoryInformation(self):
        self.assertRaises(Exception, translateMakeAnnotations, ['cmd'])

    def test_simpleDirectoryChange(self):
        self.assertEqual(
            ["cd dir1 # from make"],
            translateMakeAnnotations(["make: Entering directory 'dir1'"])
        )

    def test_twoDirectoryChanges(self):
        self.assertEqual([
            "cd dir1 # from make",
            "cd dir2 # from make",
            "cd dir2 # from make",
            "cd dir1 # from make"],
            translateMakeAnnotations([
                "make: Entering directory 'dir1'",
                "make[1]: Entering directory 'dir2'",
                "make[1]: Leaving directory 'dir2'",
                "make: Leaving directory 'dir1'"
            ])
        )
