"""
rm - remove files or directories
"""

from os import path
from ..Transformer import TransformerLlvm
from ...constants import EXECFILEEXTENSION


class TransformAr(TransformerLlvm):
    """ transform ar commands """

    @staticmethod
    def can_be_applied_on(cmd):
        return (cmd.bashcmd.startswith("rm -f ") and
                not cmd.bashcmd.startswith("rm -f -r"))

    @staticmethod
    def apply_transformation_on(cmd, container):
        # extract a list of files to be deleted
        files = cmd.bashcmd.split()[2:]

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

            # No embracing for wildcard commands
            if '*' in file:
                embrace = ""

            if file.endswith(".o"):
                # Use .bc files instead of .o files
                new.append(embrace + file[:-2] + ".bc" + embrace)
            elif file.endswith(".a") or ".so" in file:
                # simply append .bc to normal linked files
                new.append(embrace + file + ".bc" + embrace)
            elif '.' not in path.basename(file):
                # add .x.bc to executables
                new.append(
                    embrace + file + EXECFILEEXTENSION + ".bc" + embrace)

        cmd.bashcmd = "rm -f " + " ".join(new) if new else ""
        return cmd
