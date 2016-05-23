"""
rm - remove files or directories
"""

from ..Transformer import TransformerLlvm
from ...constants import EXECFILEEXTENSION


class TransformAr(TransformerLlvm):
    """ transform ar commands """

    @staticmethod
    def can_be_applied_on(cmd):
        return cmd.startswith("rm -f ")

    @staticmethod
    def apply_transformation_on(cmd, container):
        # extract a list of files to be deleted
        files = cmd.split()[2:]

        new = []
        for file in files:
            embrace = ""

            # look for embracing ' and "
            if file.startswith("'") and file.endswith("'"):
                file = file[1:-1]
                embrace = "'"
            elif file.startswith('"') and file.endswith('"'):
                file = file[1:-1]
                embrace = '"'

            if file.endswith(".o") or file.endswith(".a"):
                # simply append .bc to normal compiled files
                new.append(embrace + file + ".bc" + embrace)
            elif '.' not in file:
                # add .x.bc to executables
                new.append(
                    embrace + file + EXECFILEEXTENSION + ".bc" + embrace)

        return "rm -f " + " ".join(new) if new else ""
