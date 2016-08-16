"""
Functions for executing commands on the underlying OS
"""

from functools import wraps
from os.path import dirname, isfile
from os import chdir, environ, getcwd, sep
from subprocess import call, check_output, STDOUT, DEVNULL, CalledProcessError
from shlex import quote


def makefile_execution(func):
    """
    Small decorator for preparing and checking the environment to call make
    """
    @wraps(func)
    def wrapper(makefile, targets):
        """ Wrapper for the makefile environment"""

        # Target list is required
        if not targets:
            raise ValueError("Unknown target")

        # at first some input sanitizing
        check_makefile(makefile)
        targets = [quote(t) for t in targets]

        # save the current directory for returning to it later
        cwd = getcwd()

        # change to the directory of the makefile
        chdir(dirname(makefile))

        # Execute the decorated function
        result = func(makefile, targets)

        # return to the previous directory
        chdir(cwd)

        return result
    return wrapper


@makefile_execution
def run_make_with_debug_shell(makefile, targets):
    """ Run make and add all executed shell commands to the output """

    makedir = dirname(makefile)

    output = check_output(
        ('make --directory=%s --print-directory '
         '--quiet SHELL="sh -x" ' % makedir) + " ".join(targets),
        env=english_environment(), shell=True, stderr=STDOUT)

    # finally return the decoded output of make
    return output.decode()


@makefile_execution
def has_make_something_todo(makefile, targets):
    """ Check, if the make command actually does something """
    makedir = dirname(makefile)

    return call(
        ["make", "--directory=%s" % makedir, "--question"] + targets,
        stderr=DEVNULL, stdout=DEVNULL) != 0


def english_environment():
    """
    Create a new environment with English language
    Thereby the later parsing is deterministic
    """

    english = dict(environ)
    english['LANG'] = 'en_US.UTF-8'
    return english


def check_makefile(makefile):
    """ Several check, if the given makefile is valid makefile and exists """
    if not isfile(makefile):
        raise FileNotFoundError("No such makefile")
    if not makefile.endswith(sep + "Makefile"):
        raise FileNotFoundError("No Makefile given")


def check_clang(clang):
    """ Check if clang is a valid call to a working clang instance """

    check_version_string(
        clang,
        "OVERVIEW: clang LLVM compiler",
        "clang is not working. Please check your config.ini"
    )


def check_llvmlink(llvmlink):
    """ Check if llvmlink is a valid call to a working llvm-link instance """

    check_version_string(
        llvmlink,
        "OVERVIEW: llvm linker",
        "llvm-link is not working. Please check your config.ini"
    )


def check_version_string(cmd, outputhead, error):
    """
    Check, if a call of 'cmd --help' starts with outputhead.
    If not, an exception with with error message is raised
    """

    try:
        output = check_output([cmd, "--help"], env=english_environment())
    except FileNotFoundError:
        output = b"command not found"
    except CalledProcessError as ex:
        # Some programms return version string and non zero return codes
        output = ex.output

    # Check the head of the version output
    if not output.startswith(bytes(outputhead, "utf-8")):
        raise Exception(error)
