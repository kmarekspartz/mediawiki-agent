#!/bin/sh
ruff format .
ruff check --fix .
