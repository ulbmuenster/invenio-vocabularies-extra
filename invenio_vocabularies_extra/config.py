# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Add some extras to the vocabularies module like DDC and GND subjects.."""

from .datastreams.readers import Marc21CollectionReader

VOCABULARIES_EXTRA_SUBJECTS_DDC_LANG = "de"
"""Default lang getting mapped to vocabularies' subject."""

VOCABULARIES_EXTRA_SUBJECTS_GND_FILE_URL = (
    "https://data.dnb.de/GND/authorities-gnd-sachbegriff_dnbmarc_20241013.mrc.xml.gz"
)
"""URI to the full GND subjects authorities file."""

VOCABULARIES_DATASTREAM_READERS = {"marc21": Marc21CollectionReader}
