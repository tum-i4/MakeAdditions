from os.path import dirname, isfile
from os import chdir, environ, getcwd, sep
from subprocess import check_output


def dryRunMakefile(makefile: str, target: str ="all") -> str:
    """ Perform a dry run on makefile with the given target and returns the
        output, i.e. all the commands necessary for the build """

    # at first some input sanitizing
    if not isfile(makefile):
        raise FileNotFoundError("No such makefile")
    if not makefile.endswith(sep + "Makefile"):
        raise FileNotFoundError("No Makefile given")

    # save the current directory for returning to it later
    cwd = getcwd()

    # Create a new environment with English language
    # Thereby the later parsing is deterministic
    english = dict(environ)
    english['LANG'] = 'en_US.UTF-8'

    # change to the directory of the makefile
    chdir(dirname(makefile))

    # actually call make on this file
    output = check_output(
        ['make', "--dry-run", "--print-directory", target],
        env=english
    )

    # return to the previous directory
    chdir(cwd)

    # finally return the decoded output of make
    return output.decode()
