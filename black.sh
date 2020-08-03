#!/usr/bin/env bash

python -m black \
    --line-length 120 \
    --target-version py35 \
    --exclude "/(\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|_build|buck-out|build|dist|migrations)/" \
    .
