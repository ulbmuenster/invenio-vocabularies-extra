# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Add some extras to the vocabularies module like DDC and GND subjects.."""

from . import config


class InvenioExtraVocabularies(object):
    """invenio-vocabularies-extra extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-vocabularies-extra"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("VOCABULARIES_EXTRA_"):
                app.config.setdefault(k, getattr(config, k))
