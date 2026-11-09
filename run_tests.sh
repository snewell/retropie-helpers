#!/bin/bash

my_location=$(realpath "${BASH_SOURCE[0]}")
LIB_DIR="$(dirname "${my_location}")/../lib"

export PYTHONPATH="${PYTHONPATH}:${LIB_DIR}"

set -euo pipefail

PYTHONPATH=./lib python3 -m unittest discover -s tests
