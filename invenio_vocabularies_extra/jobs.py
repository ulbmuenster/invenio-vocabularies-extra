# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom jobs module."""
from invenio_vocabularies.jobs import ProcessDataStreamJob


class ProcessDDCJob(ProcessDataStreamJob):
    """Process DDC subjects datastream registered task."""

    description = "Process DDC subjects"
    title = "Load DDC subjects"
    id = "process_ddc_subjects"

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs):
        """Process DDC subjects."""
        return {
            "config": {
                "readers": [],
                "writers": [],
                "transformers": [],
            }
        }
