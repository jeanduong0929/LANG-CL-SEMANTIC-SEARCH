#!/bin/bash

# Check if pip3 is available
if command -v pip3 &>/dev/null; then
	# If pip3 exists, use python3
	python3 -m unittest tests.test_lab
else
	# If pip3 does not exist, use python
	python -m unittest tests.test_lab
fi
