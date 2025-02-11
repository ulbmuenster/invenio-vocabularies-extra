# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom datastream transformer for MeSH subjects."""

import lxml.etree as ET
from flask import current_app
from invenio_i18n.proxies import current_i18n
from invenio_vocabularies.datastreams.transformers import BaseTransformer

from ..config import mesh_file_url


class MeSHSubjectXMLTransformer(BaseTransformer):
    """Custom datastream transformer for GND subjects."""

    def __init__(self, *args, **kwargs):
        """Initializes the transformer."""
        super().__init__(*args, **kwargs)
        self._supported_languages = current_i18n.get_languages()

    def apply(self, stream_entry, **kwargs):
        """Transform XML data to internal format.

        Input:
           A stream_entry.entry from ZIPReader is a dict with just a "DescriptorRecord" which
           is an string.
           Record format is based on "https://www.nlm.nih.gov/databases/dtd/nlmdescriptorrecordset_20200101.dtd".
            - DescriptorUI is the ID
            - DescriptorName with <String>: starts with german title, english in brackets
              => this part is a bit tricky because other translations may as well do it differently.
            - ConceptList with tag <Concept PreferredConceptYN="Y">
            - TermList with tag <Term ConceptPreferredTermYN="N" IsPermutedTermYN="N"> is synonym

        Output:
           {
               "id": "mesh:D000003",
               "scheme": "MESH",
               "title": {
                   "de": "Schlachthöfe",
                   "en": "Abattoirs",
               },
               "subject": "Schlachthöfe",
               "synonyms": [
                   "Abattoir",
                   "Slaughter Houses",
                   "Slaughter House",
                   "Slaughterhouses",
                   "Schlachthöfe",
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
                   }
               ],
           }
        """
        record = ET.fromstring(stream_entry.entry["record"])
        default_lang = current_app.config["VOCABULARIES_EXTRA_SUBJECTS_MESH_LANG"]
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
            "scheme": "MESH",
            "synonyms": [],
            "identifiers": [],
        }
        # Extracting the main ID
        mesh_id = record.find("DescriptorUI")
        result["id"] = f"mesh:{mesh_id.text}"
        identifier = {
            "scheme": "url",
            "identifier": f"http://id.nlm.nih.gov/mesh/{mesh_id.text}",
        }
        result["identifiers"].append(identifier)
        identifier = {
            "scheme": "url",
            "identifier": f"https://id.nlm.nih.gov/mesh/{mesh_id.text}",
        }
        result["identifiers"].append(identifier)

        title = record.find("DescriptorName/String")
        if title is not None:
            open_bracket = title.text.find("[")
            close_bracket = title.text.find("]")
            title_default = title.text[:open_bracket]
            title_en = title.text[open_bracket + 1 : close_bracket]
            result["title"][default_lang] = title_default
            result["title"]["en"] = title_en
            result["subject"] = title_default

        concepts = record.findall("ConceptList/Concept")
        for concept in concepts:
            if concept.attrib["PreferredConceptYN"] == "Y":
                terms = concept.findall("TermList/Term")
                for term in terms:
                    if (
                        term.attrib["ConceptPreferredTermYN"] == "N"
                        and term.attrib["IsPermutedTermYN"] == "N"
                    ):
                        term_string = term.find("String")
                        result["synonyms"].append(term_string.text)

        stream_entry.entry = result
        return stream_entry
