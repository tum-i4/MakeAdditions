from ..TransformationTestCase import TransformationTestCase
from makeadditions.Command import Command
from makeadditions.constants import MAKEANNOTATIONHINT


class TestTransformLlvmCd(TransformationTestCase):

    def test_cd_remove_shell(self):
        self.assertTransformation("", "cd mydir")

    def test_cd_keep_make(self):
        self.assertEqual(
            Command("cd mydir", "/tmp", [MAKEANNOTATIONHINT]),
            self.llvm.transform(Command(
                "cd mydir", "/tmp", [MAKEANNOTATIONHINT]))
        )
