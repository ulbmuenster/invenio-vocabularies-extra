# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom datastream transformer for GND subjects."""

from invenio_vocabularies.datastreams import StreamEntry

from invenio_vocabularies_extra.contrib.subjects.ddc.datastreams import (
    DdcYamlTransformer,
)


def test_ddc_transformer(app, expected_ddc_result):

    ddc = {
        "id": "551",
        "en": "Geology, hydrology, meteorology",
        "de": "Geologie, Hydrologie, Meteorologie",
    }
    ddc_entry = StreamEntry(ddc)

    transformer = DdcYamlTransformer()
    assert expected_ddc_result == transformer.apply(ddc_entry).entry
