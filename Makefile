
.PHONY: all
all:
	@ echo "Please give a target. Choices are:"
	@ echo "   test -> run all unittests"

.PHONY: test
test:
	python -m unittest
