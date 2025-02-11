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

VOCABULARIES_EXTRA_SUBJECTS_MESH_LANG = "de"
"""Additional language in MeSH authorities file, must be part of I18N_LANGUAGES."""

VOCABULARIES_EXTRA_SUBJECTS_MESH_FILE_URL = (
    "https://repository.publisso.de/resource/frl:6473340/data"
)
"""URI to the MeSH authorities file. Provide an URI fitting to VOCABULARIES_EXTRA_SUBJECTS_MESH_LANG."""

VOCABULARIES_DATASTREAM_READERS = {"marc21": Marc21CollectionReader}
