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
from invenio_vocabularies.contrib.affiliations.datastreams import (
    AffiliationsServiceWriter,
)
from invenio_vocabularies.datastreams.transformers import BaseTransformer


class WikidataSPARQLTransformer(BaseTransformer):
    """Custom datastream transformer for wikidata affiliations."""

    def __init__(self, *args, **kwargs):
        """Initializes the transformer."""
        super().__init__(*args, **kwargs)
        self._supported_languages = current_i18n.get_languages()

    def apply(self, stream_entry, **kwargs):
        """
        Transform wikidata data to internal format.

        Input:
           A stream_entry.entry from SPARQLReader containing a dict with data about an organisation.

        Output:
          {
            'name': 'Max Planck Institute for Gravitational Physics',
            'country': 'DE',
            'country_name': 'Germany',
            'id': 'wd:Q2778415',
            'status': 'active',
            'title': {
              'de': 'Max-Planck-Institut für Gravitationsphysik',
              'fr': 'Institut Max-Planck de physique gravitationnelle'},
            'identifiers': [{'identifier': '03sry2h30', 'scheme': 'ror'}]
          }
        """
        org_uri = stream_entry.entry["org"].get("value", "")
        org_id = org_uri.split("/")[-1] if org_uri else ""

        org_label = stream_entry.entry["orgLabel"].get("value", "")

        element = {
            "name": org_label,
            "id": "wd:" + org_id,
            "status": "active",
        }

        i18n_labels = {}

        for lan in self._supported_languages:
            if lan[0] == "en":
                continue

            i18n_labels[lan[0]] = stream_entry.entry.get("orgLabel_" + lan[0], {}).get(
                "value", ""
            )

        element["title"] = i18n_labels

        if stream_entry.entry.get("rorID", {}):
            ror_id = stream_entry.entry.get("rorID", {}).get("value", "")

            element["identifiers"] = []
            element["identifiers"].append(
                {
                    "identifier": ror_id,
                    "scheme": "ror",
                }
            )

        if stream_entry.entry.get("acronym", {}):
            element["acronym"] = stream_entry.entry.get("acronym", {}).get("value", "")

        if stream_entry.entry.get("countryLabel", {}):
            element["country_name"] = stream_entry.entry.get("countryLabel", {}).get(
                "value", ""
            )

        if stream_entry.entry.get("countryCode", {}):
            element["country"] = stream_entry.entry.get("countryCode", {}).get(
                "value", ""
            )

        stream_entry.entry = element
        return stream_entry


VOCABULARIES_DATASTREAM_TRANSFORMERS = {
    "wikidata-affiliations": WikidataSPARQLTransformer,
}

VOCABULARIES_DATASTREAM_WRITERS = {
    "affiliations-service": AffiliationsServiceWriter,
}
