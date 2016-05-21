import unittest
from textwrap import dedent
from makelogic.parse import splitInCommands, translateMakeAnnotations


class TestPaserSplitInCommands(unittest.TestCase):

    def test_empty(self):
        self.assertEqual([], splitInCommands(""))

    def test_single_line(self):
        self.assertEqual(["gcc -v"], splitInCommands("gcc -v"))

    def test_two_lines_two_commands(self):
        self.assertEqual(["cmd1", "cmd2"], splitInCommands(dedent(
            """\
            cmd1
            cmd2
            """)))

    def test_two_lines_one_command(self):
        self.assertEqual([dedent("""\
            line 1 \\
                -line 2""")], splitInCommands(dedent("""\
            line 1 \\
                -line 2
            """)))

    def test_three_lines_two_commands(self):
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

    def test_no_directory_information(self):
        self.assertRaises(Exception, translateMakeAnnotations, ['cmd'])

    def test_simple_directory_change(self):
        self.assertEqual(
            ["cd dir1 # from make"],
            translateMakeAnnotations(["make: Entering directory 'dir1'"])
        )

    def test_two_directory_changes(self):
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
