import unittest
from makeadditions.Command import Command
from makeadditions.MakeLlvm import MakeLlvm


class TransformationTestCase(unittest.TestCase):

    def setUp(self):
        self.llvm = MakeLlvm()

    def assertTransformation(self, transformation, command, curdir="/tmp"):
        self.assertEqual(
            Command(transformation, curdir),
            self.llvm.transform(Command(command, curdir))
        )
