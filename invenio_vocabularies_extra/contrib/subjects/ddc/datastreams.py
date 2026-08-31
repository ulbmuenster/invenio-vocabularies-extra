# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom datastream transformer for GND subjects."""

from flask import current_app
from invenio_i18n.proxies import current_i18n
from invenio_vocabularies.contrib.subjects.datastreams import SubjectsServiceWriter
from invenio_vocabularies.datastreams.transformers import BaseTransformer

from ..config import oclc_ddc_url


class DdcJsonTransformer(BaseTransformer):
    """Custom datastream transformer for DDC subjects."""

    def __init__(self, *args, **kwargs):
        """Initializes the transformer."""
        super().__init__(*args, **kwargs)
        self._supported_languages = current_i18n.get_languages()

    def apply(self, stream_entry, **kwargs):
        """
        Transform OCLC Json data to internal format.

        Input:
           A stream_entry.entry is a json of the form:
            {
                "id":"https://id.oclc.org/worldcat/ddc/E3QVkT9mbHQ9brHHgvBtwj7JfQ",
                "modified":"2026-03-10T11:22:49Z",
                "prefLabel": {
                    "it":"Altre letterature germaniche",
                    "de":"Andere germanische Literaturen",
                    "fr":"Autres littératures germaniques",
                    "en":"Other Germanic literatures",
                    "sv":"Övriga germanska litteraturer",
                    "no":"Andre germanske språks litteraturer",
                    "es":"Otras literaturas germánicas"
                },
                "broader":"https://id.oclc.org/worldcat/ddc/E3VPVRyYy7TpBhRPXrFW6mp6HX",
                "type":"Concept",
                "created":"1996-06-01",
                "notation":"839",
                "inScheme":"https://id.oclc.org/worldcat/ddc/",
                "@context":"https://id.oclc.org/worldcat/ddc/context.json"
            }

        Output:
           {
               "id": "839",
               "scheme": "DDC",
               "title": {
                   "de": "Andere germanische Literaturen",
                   "en": "Other Germanic literatures",
               },
               "subject": "Andere germanische Literaturen",
               "synonyms": [],
               "identifiers": [
                   {
                       "scheme": "url",
                       "identifier": "https://id.oclc.org/worldcat/ddc/E3QVkT9mbHQ9brHHgvBtwj7JfQ",
                   }
               ],
           }
        """
        entry_data = stream_entry.entry
        default_lang = current_app.config["VOCABULARIES_EXTRA_SUBJECTS_DDC_LANG"]
        default_lang_supported = False
        for language in self._supported_languages:
            if default_lang in language:
                default_lang_supported = True
        if not default_lang_supported:
            default_lang = "en"

        result = {
            "title": {},
            "subject": "",
            "id": entry_data["notation"],
            "scheme": "DDC",
            "synonyms": [],
            "identifiers": [
                {
                    "scheme": "url",
                    "identifier": entry_data["id"],
                }
            ],
        }
        for lang in self._supported_languages:
            language_code = lang[0]
            if language_code in entry_data["prefLabel"]:
                result["title"][language_code] = entry_data["prefLabel"][
                    language_code
                ]
            if language_code == default_lang:
                result["subject"] = f"{entry_data['notation']} {entry_data['prefLabel'][language_code]}"

        stream_entry.entry = result
        return stream_entry


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
        default_lang = current_app.config["VOCABULARIES_EXTRA_SUBJECTS_DDC_LANG"]
        default_lang_supported = False
        for language in self._supported_languages:
            if default_lang in language:
                default_lang_supported = True
        if not default_lang_supported:
            default_lang = "en"

        result = {
            "title": {},
            "subject": "",
            "id": "",
            "scheme": "DDC",
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
                result["subject"] = f"{entry_data['id']} {entry_data[lang[0]]}"

        stream_entry.entry = result
        return stream_entry


VOCABULARIES_DATASTREAM_TRANSFORMERS = {
    "ddc-subjects": DdcJsonTransformer,
}


VOCABULARIES_DATASTREAM_WRITERS = {
    "subjects-service": SubjectsServiceWriter,
}


DDC_PRESET_DATASTREAM_CONFIG = {
    "readers": [
        {
            "type": "oclc-ddc",
            "args": {
                "origin": oclc_ddc_url,
                "content_type": "application/json",
            },
        },
    ],
    "transformers": [{"type": "ddc-subjects"}],
    "writers": [
        {
            "args": {"writer": {"type": "subjects-service"}},
            "type": "async",
        }
    ],
}
