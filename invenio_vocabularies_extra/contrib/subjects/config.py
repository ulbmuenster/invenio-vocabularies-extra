# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Subjects configuration."""

from flask import current_app
from werkzeug.local import LocalProxy

gnd_file_url = LocalProxy(
    lambda: current_app.config["VOCABULARIES_EXTRA_SUBJECTS_GND_FILE_URL"]
)

mesh_file_url = LocalProxy(
    lambda: current_app.config["VOCABULARIES_EXTRA_SUBJECTS_MESH_FILE_URL"]
)
