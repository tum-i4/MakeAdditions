import unittest
from textwrap import dedent
from makelogic.parse import (
    translate_makeannotations,
    extract_debugshell_and_makefile
)


class TestExtractor(unittest.TestCase):

    def test_make_statement(self):
        self.assertEqual(
            ["make: Entering directory '/tmp'"],
            extract_debugshell_and_makefile("make: Entering directory '/tmp'"))

    def test_nonsense(self):
        self.assertEqual([], extract_debugshell_and_makefile("Hello world"))

    def test_simple_command(self):
        self.assertEqual(
            ["cc -c -o main.o main.c"],
            extract_debugshell_and_makefile("+ cc -c -o main.o main.c")
        )

    def test_nested_command(self):
        self.assertEqual(
            ["cc -c -o main.o main.c"],
            extract_debugshell_and_makefile("++++ cc -c -o main.o main.c")
        )

    def test_small_block(self):
        self.assertEqual([
            "make: Entering directory '/tmp'",
            "cc -c -o main.o main.c",
            "cc -c -o divisible.o divisible.c",
            "cc -o divisible main.o divisible.o",
            "make: Leaving directory '/tmp'"],
            extract_debugshell_and_makefile(dedent("""\
            make: Entering directory '/tmp'
            + cc -c -o main.o main.c
            + cc -c -o divisible.o divisible.c
            + cc -o divisible main.o divisible.o
            make: Leaving directory '/tmp'
            """))
        )


class TestTranslateMakeAnnotations(unittest.TestCase):

    def test_empty(self):
        self.assertRaises(Exception, translate_makeannotations, [])

    def test_no_directory_information(self):
        self.assertRaises(Exception, translate_makeannotations, ['cmd'])

    def test_simple_directory_change(self):
        self.assertEqual(
            ["cd dir1 # from make"],
            translate_makeannotations(["make: Entering directory 'dir1'"])
        )

    def test_two_directory_changes(self):
        self.assertEqual([
            "cd dir1 # from make",
            "cd dir2 # from make",
            "cd dir2 # from make",
            "cd dir1 # from make"],
            translate_makeannotations([
                "make: Entering directory 'dir1'",
                "make[1]: Entering directory 'dir2'",
                "make[1]: Leaving directory 'dir2'",
                "make: Leaving directory 'dir1'"
            ])
        )
