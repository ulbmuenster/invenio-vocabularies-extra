# -*- coding: utf-8 -*-
#
# Copyright (C) 2025-2026 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


# Usage:
#   env DB=postgresql12 SEARCH=elasticsearch7 CACHE=redis MQ=rabbitmq ./run-tests.sh

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# Ensure the test extra is installed before running checks.
uv sync --extra tests --locked

# Manifest check
./.venv/bin/python -m check_manifest

# Pytests
./.venv/bin/python -m pytest
