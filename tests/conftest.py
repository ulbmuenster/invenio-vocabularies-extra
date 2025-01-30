# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from invenio_app.factory import create_app as _create_app


@pytest.fixture(scope="module")
def app_config(app_config):
    """Application config override."""
    # TODO: Override any necessary config values for tests
    app_config["VOCABULARIES_EXTRA_DDC_SUBJECT_LANG"] = "de"
    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return _create_app
