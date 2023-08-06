#!/bin/sh -ex
pip install -e .[test]
isort --check .
black --check .
flake8
pylint src/mkdocs_i18n spec/*.py
bandit -r .
mamba --enable-coverage
coverage report --fail-under=100
gitlint --commits $(git describe --tags --abbrev=0 --match "v[0-9]*" || git rev-list --max-parents=0 HEAD)..HEAD
