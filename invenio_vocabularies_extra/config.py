# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Add some extras to the vocabularies module like DDC and GND subjects.."""

from .datastreams.readers import Marc21CollectionReader

VOCABULARIES_EXTRA_DDC_SUBJECT_LANG = "de"
"""Default lang getting mapped to vocabularies' subject."""

VOCABULARIES_DATASTREAM_READERS = {"marc21": Marc21CollectionReader}
