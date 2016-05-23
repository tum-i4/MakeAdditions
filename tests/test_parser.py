import os
import unittest
from textwrap import dedent
from makelogic.constants import MAKEANNOTATIONHINT
from makelogic.parse import (
    check_debugshell_and_makefile,
    extract_debugshell,
    get_relevant_lines,
    is_noop,
    translate_to_commands,
    translate_makeannotations,
)


class TestTranslateCommands(unittest.TestCase):

    def test_make_statement(self):
        self.assertEqual(
            ["cd /tmp" + MAKEANNOTATIONHINT],
            translate_to_commands("make: Entering directory '/tmp'"))

    def test_nonsense(self):
        self.assertEqual([], translate_to_commands("Hello world"))

    def test_simple_command(self):
        self.assertEqual(
            ["cc -c -o main.o main.c"],
            translate_to_commands("+ cc -c -o main.o main.c")
        )

    def test_nested_command(self):
        self.assertEqual(
            ["cc -c -o main.o main.c"],
            translate_to_commands("++++ cc -c -o main.o main.c")
        )

    def test_small_block(self):
        self.assertEqual([
            "cd /tmp" + MAKEANNOTATIONHINT,
            "cc -c -o main.o main.c",
            "cc -c -o divisible.o divisible.c",
            "cc -o divisible main.o divisible.o",
            "cd " + os.getcwd() + MAKEANNOTATIONHINT],
            translate_to_commands(dedent("""\
            make: Entering directory '/tmp'
            + cc -c -o main.o main.c
            + cc -c -o divisible.o divisible.c
            + cc -o divisible main.o divisible.o
            make: Leaving directory '/tmp'
            """))
        )


class TestCheckDebugshellAndMakefile(unittest.TestCase):

    def test_empty(self):
        self.assertRaises(Exception, check_debugshell_and_makefile, "")

    def test_no_directory_information(self):
        self.assertRaises(Exception, check_debugshell_and_makefile, 'cmd')

    def test_normal_commands_pass(self):
        check_debugshell_and_makefile("make: Entering directory 'dir1'")


class TestExtractDebugshell(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(["cmd"], extract_debugshell(["+ cmd"]))

    def test_ignore_normal(self):
        self.assertEqual(["cd dir"], extract_debugshell(["cd dir"]))


class TestRelevantLines(unittest.TestCase):

    def test_make_is_relevant(self):
        self.assertEqual(
            ["make: Entering directory 'dir1'"],
            get_relevant_lines("make: Entering directory 'dir1'"))

    def test_debug_is_relevant(self):
        self.assertEqual(["+ cmd"], get_relevant_lines("+ cmd"))

    def test_remove_nonsense(self):
        self.assertEqual([], get_relevant_lines("nonsense"))


class TestTranslateMakeAnnotations(unittest.TestCase):

    def test_simple_directory_change(self):
        self.assertEqual(
            ["cd dir1 # from make"],
            translate_makeannotations(["make: Entering directory 'dir1'"])
        )

    def test_two_directory_changes(self):
        self.assertEqual([
            "cd dir1" + MAKEANNOTATIONHINT,
            "cmd in dir1",
            "cd dir2" + MAKEANNOTATIONHINT,
            "cmd in dir2",
            "cd dir1" + MAKEANNOTATIONHINT,
            "cmd in dir1",
            "cd " + os.getcwd() + MAKEANNOTATIONHINT,
            "cmd final"],
            translate_makeannotations([
                "make: Entering directory 'dir1'",
                "cmd in dir1",
                "make[1]: Entering directory 'dir2'",
                "cmd in dir2",
                "make[1]: Leaving directory 'dir2'",
                "cmd in dir1",
                "make: Leaving directory 'dir1'",
                "cmd final",
            ])
        )

    def test_three_directory_changes(self):
        self.assertEqual([
            "cd dir1" + MAKEANNOTATIONHINT,
            "cd dir1/dir1sub" + MAKEANNOTATIONHINT,
            "cmd in dir1sub",
            "cd dir1" + MAKEANNOTATIONHINT,
            "cmd in dir1",
            "cd " + os.getcwd() + MAKEANNOTATIONHINT,
            "cd dir2" + MAKEANNOTATIONHINT,
            "cmd in dir2",
            "cd " + os.getcwd() + MAKEANNOTATIONHINT],
            translate_makeannotations([
                "make[1]: Entering directory 'dir1'",
                "make[2]: Entering directory 'dir1/dir1sub'",
                "cmd in dir1sub",
                "make[2]: Leaving directory 'dir1/dir1sub'",
                "cmd in dir1",
                "make[1]: Leaving directory 'dir1'",
                "make[1]: Entering directory 'dir2'",
                "cmd in dir2",
                "make[1]: Leaving directory 'dir2'",
            ])
        )

    def test_target_output_is_commented(self):
        self.assertEqual(
            ["# make all" + MAKEANNOTATIONHINT],
            translate_makeannotations(["make all"])
        )
        self.assertEqual(
            ["# make my-target" + MAKEANNOTATIONHINT],
            translate_makeannotations(["make my-target"])
        )


class TestIsNoop(unittest.TestCase):

    def test_empty(self):
        self.assertTrue(is_noop(""))

    def test_spaces(self):
        self.assertTrue(is_noop("   "))

    def test_command(self):
        self.assertFalse(is_noop("cd dir"))
        self.assertFalse(is_noop("cc -c main.c"))

    def test_comment(self):
        self.assertTrue(is_noop("# comment"))

    def test_comment_with_leading_space(self):
        self.assertTrue(is_noop(" # comment"))

    def test_command_with_comment(self):
        self.assertFalse(is_noop("cd dir # change directory"))
