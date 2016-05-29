# MakeAdditions

Adds magic to your make command.

## Requirements
* Python >= 3.4

## For developers

## Requirements for development
* pyvenv (on Ubuntu: sudo apt-get install python3-venv)

### Internal structure for the executed make commands

#### Step 1: Check, whether the target must be (re)build
```
make --question all
```

#### Step 2: Perform normal, but quiet make with shell capture
```
make --print-directory --quiet SHELL="sh -x"
```

#### Step 3: Execute selected and transformed commands afterwards
```
# For more details, try:
make+llvm --just-transform
```

### Run all unit tests
```
make test
```
