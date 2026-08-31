# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Add some extras to the vocabularies module like DDC and GND subjects."""

from .ext import InvenioExtraVocabularies

__version__ = "0.4.1"

__all__ = ("__version__", "InvenioExtraVocabularies")
