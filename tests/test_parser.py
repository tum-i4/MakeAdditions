import unittest
from textwrap import dedent
from makelogic.parser import *


class TestPaser(unittest.TestCase):

    def test_splitInCommands_empty(self):
        self.assertEqual([], splitInCommands(""))

    def test_splitInCommands_singleLine(self):
        self.assertEqual(["gcc -v"], splitInCommands("gcc -v"))

    def test_splitInCommands_twoLinesTwoCommands(self):
        self.assertEqual(["cmd1", "cmd2"], splitInCommands(dedent(
            """\
            cmd1
            cmd2
            """)))

    def test_splitInCommands_twoLinesOneCommands(self):
        self.assertEqual([dedent("""\
            line 1 \\
                -line 2""")], splitInCommands(dedent("""\
            line 1 \\
                -line 2
            """)))

    def test_splitInCommands_threeLinesTwoCommands(self):
        self.assertEqual(["cmd1", dedent("""\
            line 1 \\
                -line 2""")], splitInCommands(dedent("""\
            cmd1
            line 1 \\
                -line 2
            """)))
