# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom jobs module."""
import arrow
from invenio_vocabularies.jobs import ProcessDataStreamJob

from .contrib.subjects.ddc.datastreams import DDC_PRESET_DATASTREAM_CONFIG
from .contrib.subjects.gnd.datastreams import GND_FULL_DATASTREAM_CONFIG
from .contrib.subjects.mesh.datastreams import MESH_DATASTREAM_CONFIG


class ProcessDDCJob(ProcessDataStreamJob):
    """Process DDC subjects datastream registered task."""

    description = "Process DDC subjects"
    title = "Load DDC subjects"
    id = "process_ddc_subjects"

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs):
        """Process DDC subjects."""
        return {"config": {**DDC_PRESET_DATASTREAM_CONFIG}}


class ProcessGNDSubjectsJob(ProcessDataStreamJob):
    """Process GND subjects datastream registered task."""

    description = "Import GND subjects updates"
    title = "Load GND subjects updates"
    id = "process_gnd_subjects"

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs):
        """Process GND subjects."""
        until_dt = arrow.utcnow()
        until = until_dt.format("YYYY-MM-DDTHH:mm:ss[Z]")
        if since is None:
            since_dt = until_dt.shift(minutes=-15)
        else:
            since_dt = arrow.get(since)
        since = since_dt.format("YYYY-MM-DDTHH:mm:ss[Z]")

        return {
            "config": {
                "readers": [
                    {
                        "type": "oai-pmh",
                        "args": {
                            "verb": "ListRecords",
                            "base_url": "https://services.dnb.de/oai/repository",
                            "metadata_prefix": "MARC21-xml",
                            "set": "authorities:sachbegriff",
                            "from_date": since,
                            "until_date": until,
                        },
                    },
                ],
                "transformers": [{"type": "gnd-subjects"}],
                "writers": [
                    {
                        "args": {"writer": {"type": "subjects-service"}},
                        "type": "async",
                    }
                ],
            }
        }


class ImportCompleteGndSubjectsJob(ProcessDataStreamJob):
    """Import the complete GND subjects from gzipped file."""

    description = "Import GND subjects completely"
    title = "Import complete GND subjects"
    id = "import_gnd_subjects"

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs):
        """Process GND subjects."""
        return {"config": {**GND_FULL_DATASTREAM_CONFIG}}


class ProcessMeshSubjectsJob(ProcessDataStreamJob):
    """Import the (bilingual) MeSH subjects from zipped file."""

    description = "Import (multi-lingual) MeSH subjects"
    title = "Import MeSH subjects"
    id = "import_mesh_subjects"

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs):
        """Process GND subjects."""
        return {"config": {**MESH_DATASTREAM_CONFIG}}
