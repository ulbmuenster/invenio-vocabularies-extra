# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

from flask import Flask

from invenio_vocabularies_extra import InvenioExtraVocabularies


def test_version():
    """Test version import."""
    from invenio_vocabularies_extra import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioExtraVocabularies(app)
    assert "invenio-vocabularies-extra" in app.extensions

    app = Flask("testapp")
    ext = InvenioExtraVocabularies()
    assert "invenio-vocabularies-extra" not in app.extensions
    ext.init_app(app)
    assert "invenio-vocabularies-extra" in app.extensions
