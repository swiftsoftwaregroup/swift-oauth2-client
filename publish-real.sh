#!/bin/bash

# Set the path to the .pypirc file
PYPIRC_FILE="$HOME/.pypirc"

# Function to extract credentials from the .pypirc file
get_credentials() {
  local repository=$1
  local field=$2
  grep -A2 "\[$repository\]" "$PYPIRC_FILE" | grep "$field" | awk -F' = ' '{print $2}'
}

# Extract PyPI credentials
PYPI_USERNAME=$(get_credentials "pypi" "username")
PYPI_PASSWORD=$(get_credentials "pypi" "password")

# Configure Poetry for PyPI
poetry config pypi-token.pypi "$PYPI_PASSWORD"

echo "Poetry has been configured with credentials for PyPI."

# Bump the version number
# poetry version patch  # For bug fixes
# poetry version minor  # For new features
# poetry version major  # For breaking changes

# Build the package
echo "Building the package..."
poetry build

# Publish the package
echo "Publishing the package to PyPI..."
poetry publish