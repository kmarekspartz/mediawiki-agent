#!/bin/sh
pipenv run ruff format .
pipenv run ruff check --fix .
