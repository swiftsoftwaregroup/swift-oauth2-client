#!/usr/bin/env bash

# activate virtual environment
source .venv/bin/activate

# generate and serve the docs
poetry run mkdocs serve
