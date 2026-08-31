# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Reader tests."""

from unittest.mock import call

import pytest
import requests

from invenio_vocabularies_extra.datastreams.readers import OclcDdcReader


def response(mocker, content, status_code=200):
    """Create a mocked HTTP response."""
    mocked_response = mocker.Mock(status_code=status_code)
    mocked_response.json.return_value = content
    return mocked_response


def test_oclc_ddc_reader_yields_leaves_depth_first(mocker):
    """Traverse all hierarchy levels and yield only leaves in source order."""
    origin = "https://example.org/ddc"
    top_one = "https://example.org/ddc/1"
    top_two = "https://example.org/ddc/2"
    branch = "https://example.org/ddc/1/1"
    leaf_one = "https://example.org/ddc/1/1/1"
    leaf_two = "https://example.org/ddc/1/2"
    leaf_three = "https://example.org/ddc/2/1"
    repeated_leaf = "https://example.org/ddc/repeated"
    payloads = {
        origin: {"hasTopConcept": [top_one, top_two]},
        top_one: {"id": "1", "narrower": [branch, leaf_two, repeated_leaf]},
        branch: {"id": "1.1", "narrower": [leaf_one]},
        leaf_one: {"id": "1.1.1", "prefLabel": {"en": "Something"}},
        leaf_two: {"id": "1.2", "prefLabel": {"en": "Something"}},
        top_two: {"id": "2", "narrower": [leaf_three, repeated_leaf]},
        leaf_three: {"id": "2.1", "prefLabel": {"en": "Something"}},
        repeated_leaf: {"id": "repeated", "prefLabel": {"en": "Something"}},
    }
    get = mocker.patch(
        "invenio_vocabularies_extra.datastreams.readers.requests.get",
        side_effect=lambda url, **kwargs: response(mocker, payloads[url]),
    )
    reader = OclcDdcReader(origin=origin, content_type="application/json")

    assert list(reader.read()) == [
        {"id": "1.1.1", "prefLabel": {"en": "Something"}},
        {"id": "1.2", "prefLabel": {"en": "Something"}},
        {"id": "repeated", "prefLabel": {"en": "Something"}},
        {"id": "2.1", "prefLabel": {"en": "Something"}},
        {"id": "repeated", "prefLabel": {"en": "Something"}},
    ]
    headers = {"Accept": "application/json"}
    assert get.call_args_list == [
        call(origin, headers=headers),
        call(top_one, headers=headers),
        call(branch, headers=headers),
        call(leaf_one, headers=headers),
        call(leaf_two, headers=headers),
        call(repeated_leaf, headers=headers),
        call(top_two, headers=headers),
        call(leaf_three, headers=headers),
        call(repeated_leaf, headers=headers),
    ]


def test_oclc_ddc_reader_raises_for_failed_request(mocker):
    """Abort traversal when any hierarchy request is unsuccessful."""
    origin = "https://example.org/ddc"
    failed_url = "https://example.org/ddc/1"
    get = mocker.patch(
        "invenio_vocabularies_extra.datastreams.readers.requests.get",
        side_effect=[
            response(mocker, {"hasTopConcept": [failed_url]}),
            response(mocker, {}, status_code=503),
        ],
    )
    reader = OclcDdcReader(origin=origin, content_type="application/json")

    with pytest.raises(requests.HTTPError, match=f"{failed_url}: 503"):
        list(reader.read())

    assert get.call_count == 2
