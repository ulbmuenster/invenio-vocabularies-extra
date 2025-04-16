# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Extra Readers module."""

from invenio_i18n.proxies import current_i18n
from invenio_vocabularies.datastreams.readers import BaseReader
from lxml import etree

# "sparql"
try:
    import SPARQLWrapper as sparql
except ImportError:
    sparql = None


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


class WikidataAffiliationsReader(BaseReader):
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
            bd:serviceParam wikibase:language \"en\".
            }}
        }}
        """

        self._origin = origin
        self._query = query
        super().__init__(origin=origin, query=query, mode=mode, *args, **kwargs)

    def _iter(self, fp, *args, **kwargs):
        raise NotImplementedError(
            "WikidataAffiliationsReader downloads one result set from the wikidata SPARQL endpoint and therefore does not iterate through items"
        )

    def read(self, item=None, *args, **kwargs):
        """Fetch and process RDF data, yielding results one at a time."""
        if item:
            raise NotImplementedError(
                "SPARQLReader does not support being chained after another reader"
            )

        # Add user agent as wikidata policies require
        user_agent = "InvenioRDMVocabulariesExtra/1.0.0 (https://github.com/ulbmuenster/invenio-vocabularies-extra)"

        sparql_client = sparql.SPARQLWrapper(self._origin, agent=user_agent)

        sparql_client.setQuery(self._query)
        sparql_client.setReturnFormat(sparql.JSON)

        results = sparql_client.query().convert()
        yield from results["results"]["bindings"]
