#!/bin/bash

# activate virtual environment
source .venv/bin/activate

# publish the docs
poetry run mkdocs gh-deploy