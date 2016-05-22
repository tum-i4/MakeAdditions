import unittest
from os import linesep
from makelogic.MakeLlvm import MakeLlvm


class TestTransformMulti(unittest.TestCase):

    def setUp(self):
        self.klee = MakeLlvm()

    def test_ranlib(self):
        self.assertEqual(linesep * 4, self.klee.transform(
            "if ( test -f ranlib -o -f /usr/bin/ranlib -o \\\n"
            "\t-f /bin/ranlib -o -f /usr/ccs/bin/ranlib ) ; then \\\n"
            "\techo ranlib libbz2.a ; \\\n"
            "\tranlib libbz2.a ; \\\n"
            "fi"))
