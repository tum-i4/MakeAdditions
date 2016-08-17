from ..TransformationTestCase import TransformationTestCase
from makeadditions.constants import EXECFILEEXTENSION


class TestTransformLlvmRm(TransformationTestCase):

    def test_rm_single_object_file(self):
        self.assertTransformation("rm -f main.bc", "rm -f main.o")

    def test_rm_single_static_library(self):
        self.assertTransformation("rm -f lib.a.bc", "rm -f lib.a")

    def test_rm_single_executable(self):
        self.assertTransformation(
            "rm -f executable" + EXECFILEEXTENSION + ".bc",
            "rm -f executable")

    def test_no_rm_for_single_irrelevant(self):
        self.assertTransformation("", "rm -f notrelevant.sh")

    def test_no_rm_for_two_irrelevant(self):
        self.assertTransformation("", "rm -f one.sh two.sh")

    def test_rm_wildcard_object(self):
        self.assertTransformation("rm -f *.bc", "rm -f *.o")

    def test_rm_wildcard_enquoted(self):
        self.assertTransformation("rm -f *.bc", "rm -f '*.o'")

    def test_rm_mixed_bzip2(self):
        self.assertTransformation(
            "rm -f *.bc libbz2.a.bc bzip2" + EXECFILEEXTENSION +
            ".bc bzip2recover" + EXECFILEEXTENSION + ".bc",
            "rm -f '*.o' libbz2.a bzip2 bzip2recover sample1.rb2"
        )

    def test_rm_recursive_tar(self):
        self.assertTransformation("", "rm -f -r testsuite.dir testsuite.log")
