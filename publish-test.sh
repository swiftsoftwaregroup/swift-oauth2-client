#!/bin/bash

# Set the path to the .pypirc file
PYPIRC_FILE="$HOME/.pypirc"

# Function to extract credentials from the .pypirc file
get_credentials() {
  local repository=$1
  local field=$2
  grep -A2 "\[$repository\]" "$PYPIRC_FILE" | grep "$field" | awk -F' = ' '{print $2}'
}

# Extract TestPyPI credentials
TESTPYPI_USERNAME=$(get_credentials "testpypi" "username")
TESTPYPI_PASSWORD=$(get_credentials "testpypi" "password")

# Configure Poetry for TestPyPI
poetry config pypi-token.testpypi "$TESTPYPI_PASSWORD"
poetry config repositories.testpypi https://test.pypi.org/legacy/

echo "Poetry has been configured with credentials for TestPyPI."

# Bump the version number
# poetry version patch  # For bug fixes
poetry version minor  # For new features
# poetry version major  # For breaking changes

# Build the package
echo "Building the package..."
poetry build

# Publish the package
echo "Publishing the package to TestPyPI..."
poetry publish --repository testpypi