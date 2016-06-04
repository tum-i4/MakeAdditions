import unittest
from makeadditions.Command import Command


class TestCommandIsNoop(unittest.TestCase):

    def test_empty(self):
        self.assertTrue(Command("", "/tmp").is_noop())

    def test_spaces(self):
        self.assertTrue(Command("   ", "/tmp").is_noop())

    def test_command(self):
        self.assertFalse(Command("cd dir", "/tmp").is_noop())
        self.assertFalse(Command("cc -c main.c", "/tmp").is_noop())

    def test_comment(self):
        self.assertTrue(Command("# comment", "/tmp").is_noop())

    def test_comment_with_leading_space(self):
        self.assertTrue(Command(" # comment", "/tmp").is_noop())

    def test_command_with_comment(self):
        self.assertFalse(
            Command("cd dir # change directory", "/tmp").is_noop())
