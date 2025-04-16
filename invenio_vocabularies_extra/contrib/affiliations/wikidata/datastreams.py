# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom datastream transformer for wikidata affiliations."""

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
           A stream_entry.entry from WikidataAffiliationsReader containing a dict with data about an organisation.
           It contains the following entries, each with nested "value", "type" and (in case of labels) "xml:lang" fields:
           org, orgLabel, acronym, countryLabel, CountryCode, rorID and one orgLabel_<lan> for each language configured in the instance.
           Only org and orgLabel are required to be always present.

        Output:
          {
            'name': 'Max Planck Institute for Gravitational Physics',
            'country': 'DE',
            'country_name': 'Germany',
            'id': 'wikidata:Q2778415',
            'status': 'active',
            'title': {
              'en': 'Max Planck Institute for Gravitational Physics',
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
            "id": "wikidata:" + org_id,
            "status": "active",
        }

        i18n_labels = {}

        for lan in self._supported_languages:
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
    "wikidata": WikidataSPARQLTransformer,
}

VOCABULARIES_DATASTREAM_WRITERS = {
    "affiliations-service": AffiliationsServiceWriter,
}

WIKIDATA_PRESET_DATASTREAM_CONFIG = {
    "readers": [
        {
            "type": "wikidata",
            "args": {
                "search_space": """
                    {
                       ?org wdt:P31?type.
                        VALUES?type {
                          wd:Q875538
                          wd:Q161057
                          wd:Q6019423
                          wd:Q1365560
                          wd:Q20168706
                        }
                      }
                      UNION
                      {
                       ?org wdt:P463?parentType.
                        VALUES?parentType {
                          wd:Q679913
                          wd:Q680090
                          wd:Q158085
                        }
                      }

                    ?org wdt:P17 wd:Q183.
                    """,
            },
        },
    ],
    "transformers": [{"type": "wikidata"}],
    "writers": [
        {
            "args": {"writer": {"type": "affiliations-service"}},
            "type": "async",
        }
    ],
}
