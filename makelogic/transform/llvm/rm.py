"""
rm - remove files or directories
"""

from ..Transformer import TransformerLlvm


class TransformAr(TransformerLlvm):
    """ transform ar commands """

    @staticmethod
    def can_be_applied_on(cmd: str) -> bool:
        return cmd.startswith("rm -f ")

    @staticmethod
    def apply_transformation_on(cmd: str, container) -> str:
        # extract a list of files to be deleted
        files = cmd.split()[2:]

        new = []
        for file in files:
            embrace = ""

            # look for ' and "
            if file.startswith("'") and file.endswith("'"):
                file = file[1:-1]
                embrace = "'"
            elif file.startswith('"') and file.endswith('"'):
                file = file[1:-1]
                embrace = '"'

            if file.endswith(".o") or file.endswith(".a"):
                new.append(embrace + file + ".bc" + embrace)
            elif '.' not in file:
                new.append(embrace + file + ".x.bc" + embrace)

        return "rm -f " + " ".join(new) if new else ""
