#!/bin/bash

set -e

TAG=$(uv run --no-sync python -c 'import tomllib; print("v" + tomllib.loads(open("pyproject.toml").read())["project"]["version"])')

read -p "Creating new release for $TAG. Do you want to continue? [Y/n] " prompt

if [[ $prompt == "y" || $prompt == "Y" || $prompt == "yes" || $prompt == "Yes" ]]; then
    git add -A
    git commit -m "Bump version to $TAG for release" || true && git push
    echo "Creating new git tag $TAG"
    git tag "$TAG" -m "$TAG"
    git push --tags
else
    echo "Cancelled"
    exit 1
fi
