# MakeLogic

Use the logic of a Makefile

## Requirements
* Python >= 3.4

## For developers

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
make+llvm --dry-run
```

### Run all unit tests
```
python -m unittest
```
