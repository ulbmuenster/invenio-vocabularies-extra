..
    Copyright (C) 2025 University of Münster.

    invenio-vocabularies-extra is free software; you can redistribute it
    and/or modify it under the terms of the MIT License; see LICENSE file for
    more details.

============================
 invenio-vocabularies-extra
============================

Add some extras to the vocabularies module like DDC and GND subjects.

This module is based on `invenio-vocabularies` and offers additional readers, transformers and job.

:Readers:
    *Marc21CollectionReader* for a one-time import of Marc21-xml formatted authority collections

:Transformers:
    *DdcYamlTransformer* for transformation of a yaml based DDC source file
    *GNDSubjectMarc21Transformer* to transform GND subjects

:Jobs:
    *ProcessDDCJob* for an import of DDC subjects (to level 3) in different languages
    *ImportCompleteGndSubjectsJob* for a one-time import of a GND authorities file
    *ProcessGNDSubjectsJob* for a regular OAI-PMH based harvesting of GND authorities



