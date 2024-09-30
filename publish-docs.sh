#!/bin/bash

# activate virtual environment
source .venv/bin/activate

# generate and serve the docs
poetry run mkdocs serve

# publish the docs
poetry run mkdocs gh-deploy