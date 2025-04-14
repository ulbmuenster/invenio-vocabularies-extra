# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Extra Readers module."""

from invenio_i18n.proxies import current_i18n
from invenio_vocabularies.datastreams.readers import BaseReader, SPARQLReader
from lxml import etree


class Marc21CollectionReader(BaseReader):
    """Reader for MARC21 collection data."""

    def _iter(self, fp, *args, **kwargs):
        """Yields single records from Marc21-xml collection."""
        collection = etree.parse(fp)
        xmlns = "{http://www.loc.gov/MARC21/slim}"
        records = collection.findall(f"{xmlns}record")
        for record in records:
            yield {"record": etree.tostring(record)}


class MeshReader(BaseReader):
    """Reader for MeSH xml data."""

    def _iter(self, fp, *args, **kwargs):
        """Yields single records from MeSH-xml descriptorRecordSet."""
        descriptorRecordSet = etree.parse(fp)
        descriptorRecords = descriptorRecordSet.findall("DescriptorRecord")
        for descriptorRecord in descriptorRecords:
            yield {"record": etree.tostring(descriptorRecord)}


class WikidataAffiliationsReader(SPARQLReader):
    """Reader class to fetch and process affiliations data from Wikidata."""

    def __init__(self, search_space, mode="r", *args, **kwargs):
        """Initialize the reader with the data source.

        :param search_space: Additional conditions for which items should be retrieved from wikidata.
        :param mode: Mode of operation (default is 'r' for reading).
        """
        origin = "https://query.wikidata.org/sparql"

        languages = current_i18n.get_languages()
        i18n_labels = ""
        i18n_rdfs_label = ""
        for lan in languages:
            i18n_labels += f"?orgLabel_{lan[0]}"
            i18n_rdfs_label += f'OPTIONAL {{?org rdfs:label?orgLabel_{lan[0]} FILTER (lang(?orgLabel_{lan[0]}) = "{lan[0]}"). }}\n'

        query = f"""
        SELECT DISTINCT ?org ?orgLabel {i18n_labels} ?countryLabel ?countryCode ?acronym ?rorID
            WHERE {{
            {search_space}

            ?org wdt:P17?country.

            OPTIONAL {{?country rdfs:label?countryLabel FILTER (lang(?countryLabel) = \"en\"). }}
            OPTIONAL {{?country wdt:P297?countryCode. }}

            OPTIONAL {{?org wdt:P1813?acronym. }}
            OPTIONAL {{?org wdt:P6782?rorID. }}
            {i18n_rdfs_label}

            SERVICE wikibase:label {{
            bd:serviceParam wikibase:language \"[AUTO_LANGUAGE],en\".
            }}
        }}
        """

        self._origin = origin
        self._query = query
        super().__init__(origin=origin, query=query, mode=mode, *args, **kwargs)
