# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom datastream transformer for GND subjects."""
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_i18n.proxies import current_i18n
from invenio_vocabularies.contrib.subjects.datastreams import SubjectsServiceWriter
from invenio_vocabularies.datastreams.transformers import BaseTransformer


class DdcYamlTransformer(BaseTransformer):
    """Custom datastream transformer for DDC subjects."""

    def __init__(self, *args, **kwargs):
        """Initializes the transformer."""
        super().__init__(*args, **kwargs)
        self._supported_languages = current_i18n.get_languages()

    def apply(self, stream_entry, **kwargs):
        """
        Transform YAML data to internal format.

        Input:
           A stream_entry.entry is a dict with the values:
           - id
           - en
           - de

        Output:
           {
               "id": "551",
               "scheme": "DDC",
               "title": {
                   "de": "Geologie, Hydrologie, Meteorologie",
                   "en": "Geology, hydrology, meteorology",
               },
               "subject": "Geologie, Hydrologie, Meteorologie",
               "synonyms": [],
               "identifiers": [
                   {
                       "scheme": "url",
                       "identifier": "http://dewey.info/551",
                   }
               ],
           }
        """
        entry_data = stream_entry.entry
        default_lang = current_app.config["VOCABULARIES_EXTRA_DDC_SUBJECT_LANG"]
        if default_lang not in self._supported_languages:
            default_lang = "en"

        result = {
            "title": {},
            "subject": "",
            "id": "",
            "scheme": "GND",
            "synonyms": [],
            "identifiers": [],
        }
        result["id"] = entry_data["id"]
        identifier = {
            "scheme": "url",
            "identifier": f"http://dewey.info/{entry_data['id']}",
        }
        result["identifiers"].append(identifier)
        for lang in self._supported_languages:
            if lang[0] in entry_data:
                result["title"][lang[0]] = entry_data[lang[0]]
            if lang[0] == default_lang:
                result["subject"] = entry_data[lang[0]]

        stream_entry.entry = result
        return stream_entry


VOCABULARIES_DATASTREAM_TRANSFORMERS = {
    "ddc-ubjects": DdcYamlTransformer,
}


VOCABULARIES_DATASTREAM_WRITERS = {
    "subjects-service": SubjectsServiceWriter,
}


DATASTREAM_CONFIG = {
    "readers": [
        {
            "type": "oaireader",
            "args": {
                "verb": "ListRecords",
                "base_url": "https://services.dnb.de/oai/repository",
                "metadata_prefix": "MARC21-xml",
                "set": "authorities:sachbegriff",
                "from": "now-10min",
                "until": "now",
            },
        },
    ],
    "transformers": [{"type": "ddc-subjects"}],
    "writers": [
        {
            "type": "subjects-service",
            "args": {
                "identity": system_identity,
            },
        }
    ],
}
