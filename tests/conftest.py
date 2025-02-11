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

import tempfile

import pytest
from flask import Flask
from invenio_app.factory import create_app as _create_app
from invenio_i18n import InvenioI18N


@pytest.fixture(scope="module")
def app_config(app_config):
    """Application config override."""
    # TODO: Override any necessary config values for tests
    app_config["VOCABULARIES_EXTRA_SUBJECTS_DDC_LANG"] = "de"
    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return _create_app


@pytest.fixture()
def base_app():
    """Flask base application fixture."""
    instance_path = tempfile.mkdtemp()
    app_ = Flask("testapp", instance_path=instance_path)
    app_.config.update(
        VOCABULARIES_EXTRA_SUBJECTS_DDC_LANG="de",
        VOCABULARIES_EXTRA_SUBJECTS_MESH_LANG="de",
        ACCOUNTS_USE_CELERY=False,
        SECRET_KEY="CHANGE_ME",
        SECURITY_PASSWORD_SALT="CHANGE_ME_ALSO",
        TESTING=True,
        I18N_LANGUAGES=[
            ("de", "German"),
        ],
    )

    InvenioI18N(app_)
    return app_


@pytest.fixture()
def app(base_app, request):
    """Flask application fixture."""
    return base_app


@pytest.fixture(scope="module")
def expected_ddc_result():
    """Set the expected results."""
    return {
        "id": "551",
        "identifiers": [{"identifier": "http://dewey.info/551", "scheme": "url"}],
        "scheme": "DDC",
        "subject": "551 Geologie, Hydrologie, Meteorologie",
        "title": {
            "en": "Geology, hydrology, meteorology",
            "de": "Geologie, Hydrologie, Meteorologie",
        },
        "synonyms": [],
    }


@pytest.fixture(scope="module")
def expected_mesh_result():
    """Set the expected results."""
    return {
        "id": "mesh:D000003",
        "scheme": "MESH",
        "title": {
            "de": "Schlachthöfe",
            "en": "Abattoirs",
        },
        "subject": "Schlachthöfe",
        "synonyms": [
            "Slaughter Houses",
            "Slaughter House",
            "Slaughterhouses",
            "Schlachthoefe",
            "Schlachthäuser",
            "Schlachthaeuser",
        ],
        "identifiers": [
            {
                "scheme": "url",
                "identifier": "http://id.nlm.nih.gov/mesh/D000003",
            },
            {
                "scheme": "url",
                "identifier": "https://id.nlm.nih.gov/mesh/D000003",
            },
        ],
    }
