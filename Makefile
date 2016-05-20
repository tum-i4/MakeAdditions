
.PHONY: all
all:
	@ echo "Please give a target. Choices are:"
	@ echo "   test -> run all unittests"
	@ echo "   venv -> update (and if needed initialize) the virual environment"

.PHONY: test
test: venv
	.venv/bin/python -m unittest

# Initialize the virtual environment, if needed
.venv:
	pyvenv .venv

# Install and keep in sync with the requirements
.venv/bin/activate: requirements.txt .venv
	.venv/bin/pip install -Ur requirements.txt
	touch .venv/bin/activate

.PHONY: venv
venv: .venv/bin/activate
