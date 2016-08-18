# MakeAdditions

*Add magic to your make command.*

This is a python package, that encapsulate calls to make and thereby generate additional deliverables. For example it can generate llvm bitcode equivalents for all generated binaries. Most import, you do not have to change any file for this - no code, no make rule, nothing.

Nearly all unix programs share the same process: `./configure, make, make install`. I just slightly adopted this process and leave the rest to this python package. All you need is `./configure CC=clang, make+llvm`

I came up with the idea for this project during some experiments with [symbolic program execution](https://en.wikipedia.org/wiki/Symbolic_execution) and automatic error detection. I want to try [KLEE](https://klee.github.io/) on different projects, but I find it pretty hard and ugly to emit llvm bitcode for programs older than llvm itself. Even the [official tutorial for testing coreutils](https://klee.github.io/tutorials/testing-coreutils/) doesn't work with my LLVM 3.4.

I am aware of the complexity within the make process and even worse, the possibilities of the shell, but I hope this project can be extended easily enough to new, unseen makefiles. Nevertheless, every command can be displayed and executed by hand, if all automation fails.

## Requirements

For the most minimal setup of this package, you need at least **Python >= 3.4**.
On ubuntu you may run: `sudo apt-get install python3`

In order to build anything useful, you need a **working compiler**. For program analysis, e.g. running [KLEE](https://klee.github.io/), I prefer using my own self-compiled llvm toolchain, but plain old standard installation works as well. On ubuntu you may run: `sudo apt-get install build-essential lvm clang`

Finally, if you are a developer - or at least, you want to modify this package - it is quite handy to use a local virtual environment and install this package in there. For this purpose this package uses python's native approach [**venv**](https://docs.python.org/dev/library/venv.html). On ubuntu you may run: `sudo apt-get install python3-venv`

## make+llvm: Compile your project as llvm bitcode

Warning: Please keep in mind, that `make+llvm` includes a casual run of `make`. Therefore, just simply replace all your calls to `make ...` with `make+llvm ...` and everything works fine, even `make+llvm clean`

`make+llvm` generates additional llvm-bitcode versions of all files, that are compiled and/or linked during the normal build process with `make`. In more details, you get the following files in the same directory additional to the normal make target deliverables.

```
*.o           -> *.bc
executable    -> executable.x.bc
*.a           -> *.a.bc
*.so.VERSION  -> *.so.VERSION.bc
```

## Main landmarks during the make process with additions

MakeAdditions aims to be very close to the normal semantics of make, e.i have very minimalistic commands (`make+llvm <target>`) and only rebuild, what was changed earlier. Nevertheless, thousands of commands are executed in the background and only one erroneous call can stop the whole compilation process. When digging for errors, remember this basic main commands, that are hidden in the internals of make+llvm.

### Step 0: Before doing anything: is make really working?
```
make <target>
```

This command is not executed by make+llvm, but can safe hours of debugging. If the normal make process is not working, something is wrong on your system and must be fixed. make+llvm do not work, until make finishes properly.

### Step 1: Check, whether the target must be (re)build
```
make --question <target>
```

First of all, make only rebuilds targets, that are "new" or "changed" since the last call. Rebuilding this logic completely is unnecessary, because make has a --question flags, that asks make, if there is anything todo. make+llvm continues only, if there is something to do.

### Step 2: Perform normal, but quiet make with shell capture
```
make --print-directory --quiet SHELL="bash -x" <target>
```

The next step is a "normal" call of make for the given target - it just uses some weired flags for the call. The most important one is `SHELL="bash -x"`. It basically prints all commands with inserted variables before they are executed. This produces a lot of output, but each command, that is invoked during make, even if it is hidden in another .sh-file, is printed with a "+" in the head of the line. (run `help set` for more details)

There is only one downside: You get no information, in which directory you are working. Therefore, the `--print-directory` flag is given, which tells make to add additional information to the output, whenever it is entering or leaving a directory.

The last remaining problem is, that the regular output of make pollutes the information from these flags. The `--quiet` flag suppress most of this output.

If you find it hard to read the plain output of the whole command, you can run the following command to get a more prefiltered version.

```
make+llvm --just-record <target>
```

### Step 3: Transform selected commands

In the next step, all the previously recorded commands are transformed for the corresponding build addition. Normally a lot of the commands are not relevant for the additional build (e.g. creation of local variables, debug echo statements). The remaining commands are transformed to build their new target. For `make+llvm` everything is transformed to emit llvm bitcode.

```
make+llvm --just-transform <target>
```

You may notice, that the output of this command contains a lot of empty lines. This is intentional. In this way, the line numbers matches the numbers from the previous `--just-record` flag and it is way easier to track, which commands belongs together and which commands are skipped.

### Step 4: Execute the transformed commands

Finally, all the transformed commands are executed in the same order as the original commands. Unfortunately, this execution only works on a single thread, because no information about independent commands remains in their serial record.

## Notes for developers

This project uses a makefile for the most common tasks. Simply run `make` in the main directory in order to get a list of all commands. If you want to submit pull requests, please make sure, that `make test` still works and `pylint makeadditions` reports no errors.

### Getting started
For the lazy people: these commands are a good starting point.

```
make dev
source .venv/bin/activate
make+llvm -h
```

### How to add own transformation

* **Step 1**: Try to isolate the command [see Main landmarks for details](#main-landmarks-during the-make-process-with-additions)
* **Step 2**: Add a new test case to `tests/transform/ADDITION/test_COMMAND.py`
* **Step 3**: Change the corresponding `makeadditions/transform/ADDITION/COMMAND.py` till all tests pass

If you want to transform a new kind command, just create new files in the corresponding directories. The transformation is registered automatically, as long as the new transformer class inherit from the `TransformerLlvm` class. Thereby you normally don't have to change any other file than the two mentioned above. The `cd` transformer is a good point to start.
