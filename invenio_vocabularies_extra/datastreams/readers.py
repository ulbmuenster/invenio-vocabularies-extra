# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Extra Readers module."""

from invenio_vocabularies.datastreams.readers import BaseReader
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
