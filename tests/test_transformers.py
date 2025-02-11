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
from invenio_vocabularies_extra.contrib.subjects.mesh.datastreams import (
    MeSHSubjectXMLTransformer,
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


def test_mesh_transformer(app, expected_mesh_result):
    mesh_descriptor = """
        <DescriptorRecord DescriptorClass="1">
          <DescriptorUI>D000003</DescriptorUI>
          <DescriptorName>
            <String>Schlachthöfe[Abattoirs]</String>
          </DescriptorName>
          <DateCreated>
            <Year>1999</Year>
            <Month>01</Month>
            <Day>01</Day>
          </DateCreated>
          <DateRevised>
            <Year>2016</Year>
            <Month>06</Month>
            <Day>08</Day>
          </DateRevised>
          <DateEstablished>
            <Year>1966</Year>
            <Month>01</Month>
            <Day>01</Day>
          </DateEstablished>
          <AllowableQualifiersList>
            <AllowableQualifier>
              <QualifierReferredTo>
                <QualifierUI>Q000145</QualifierUI>
                <QualifierName>
                  <String>classification</String>
                </QualifierName>
              </QualifierReferredTo>
              <Abbreviation>CL</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
              <QualifierReferredTo>
                <QualifierUI>Q000191</QualifierUI>
                <QualifierName>
                  <String>economics</String>
                </QualifierName>
              </QualifierReferredTo>
              <Abbreviation>EC</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
              <QualifierReferredTo>
                <QualifierUI>Q000266</QualifierUI>
                <QualifierName>
                  <String>history</String>
                </QualifierName>
              </QualifierReferredTo>
              <Abbreviation>HI</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
              <QualifierReferredTo>
                <QualifierUI>Q000331</QualifierUI>
                <QualifierName>
                  <String>legislation &amp; jurisprudence</String>
                </QualifierName>
              </QualifierReferredTo>
              <Abbreviation>LJ</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
              <QualifierReferredTo>
                <QualifierUI>Q000458</QualifierUI>
                <QualifierName>
                  <String>organization &amp; administration</String>
                </QualifierName>
              </QualifierReferredTo>
              <Abbreviation>OG</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
              <QualifierReferredTo>
                <QualifierUI>Q000592</QualifierUI>
                <QualifierName>
                  <String>standards</String>
                </QualifierName>
              </QualifierReferredTo>
              <Abbreviation>ST</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
              <QualifierReferredTo>
                <QualifierUI>Q000600</QualifierUI>
                <QualifierName>
                  <String>supply &amp; distribution</String>
                </QualifierName>
              </QualifierReferredTo>
              <Abbreviation>SD</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
              <QualifierReferredTo>
                <QualifierUI>Q000639</QualifierUI>
                <QualifierName>
                  <String>trends</String>
                </QualifierName>
              </QualifierReferredTo>
              <Abbreviation>TD</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
              <QualifierReferredTo>
                <QualifierUI>Q000706</QualifierUI>
                <QualifierName>
                  <String>statistics &amp; numerical data</String>
                </QualifierName>
              </QualifierReferredTo>
              <Abbreviation>SN</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
              <QualifierReferredTo>
                <QualifierUI>Q000941</QualifierUI>
                <QualifierName>
                  <String>ethics</String>
                </QualifierName>
              </QualifierReferredTo>
              <Abbreviation>ES</Abbreviation>
            </AllowableQualifier>
          </AllowableQualifiersList>
          <NLMClassificationNumber>WA 707</NLMClassificationNumber>
          <TreeNumberList>
            <TreeNumber>J01.576.423.200.700.100</TreeNumber>
            <TreeNumber>J03.540.020</TreeNumber>
          </TreeNumberList>
          <ConceptList>
            <Concept PreferredConceptYN="Y">
              <ConceptUI>M0000003</ConceptUI>
              <ConceptName>
                <String>Schlachthöfe[Abattoirs]</String>
              </ConceptName>
              <ScopeNote>Places where animals are slaughtered and dressed for market.
            </ScopeNote>
              <TermList>
                <Term ConceptPreferredTermYN="Y" IsPermutedTermYN="N" LexicalTag="NON" RecordPreferredTermYN="Y">
                  <TermUI>T000009</TermUI>
                  <String>Abattoirs</String>
                  <DateCreated>
                    <Year>1999</Year>
                    <Month>01</Month>
                    <Day>01</Day>
                  </DateCreated>
                  <ThesaurusIDlist>
                    <ThesaurusID>NLM (1966)</ThesaurusID>
                  </ThesaurusIDlist>
                </Term>
                <Term ConceptPreferredTermYN="N" IsPermutedTermYN="Y" LexicalTag="NON" RecordPreferredTermYN="N">
                  <TermUI>T000009</TermUI>
                  <String>Abattoir</String>
                </Term>
                <Term ConceptPreferredTermYN="N" IsPermutedTermYN="N" LexicalTag="NON" RecordPreferredTermYN="N">
                  <TermUI>T000901742</TermUI>
                  <String>Slaughter Houses</String>
                  <DateCreated>
                    <Year>2016</Year>
                    <Month>05</Month>
                    <Day>25</Day>
                  </DateCreated>
                  <ThesaurusIDlist>
                    <ThesaurusID>NLM (2017)</ThesaurusID>
                  </ThesaurusIDlist>
                </Term>
                <Term ConceptPreferredTermYN="N" IsPermutedTermYN="Y" LexicalTag="NON" RecordPreferredTermYN="N">
                  <TermUI>T000901742</TermUI>
                  <String>House, Slaughter</String>
                </Term>
                <Term ConceptPreferredTermYN="N" IsPermutedTermYN="Y" LexicalTag="NON" RecordPreferredTermYN="N">
                  <TermUI>T000901742</TermUI>
                  <String>Houses, Slaughter</String>
                </Term>
                <Term ConceptPreferredTermYN="N" IsPermutedTermYN="N" LexicalTag="NON" RecordPreferredTermYN="N">
                  <TermUI>T000901743</TermUI>
                  <String>Slaughter House</String>
                  <DateCreated>
                    <Year>2016</Year>
                    <Month>05</Month>
                    <Day>25</Day>
                  </DateCreated>
                  <ThesaurusIDlist>
                    <ThesaurusID>NLM (2017)</ThesaurusID>
                  </ThesaurusIDlist>
                </Term>
                <Term ConceptPreferredTermYN="N" IsPermutedTermYN="N" LexicalTag="NON" RecordPreferredTermYN="N">
                  <TermUI>T000010</TermUI>
                  <String>Slaughterhouses</String>
                  <DateCreated>
                    <Year>1974</Year>
                    <Month>03</Month>
                    <Day>29</Day>
                  </DateCreated>
                  <ThesaurusIDlist>
                    <ThesaurusID>UNK (19XX)</ThesaurusID>
                  </ThesaurusIDlist>
                </Term>
                <Term ConceptPreferredTermYN="N" IsPermutedTermYN="Y" LexicalTag="NON" RecordPreferredTermYN="N">
                  <TermUI>T000010</TermUI>
                  <String>Slaughterhouse</String>
                </Term>
                <Term ConceptPreferredTermYN="Y" IsPermutedTermYN="N" LexicalTag="NON" RecordPreferredTermYN="Y">
                  <TermUI>ger0000003</TermUI>
                  <String>Schlachthöfe</String>
                  <DateCreated>
                    <Year>2003</Year>
                    <Month>04</Month>
                    <Day>25</Day>
                  </DateCreated>
                </Term>
                <Term ConceptPreferredTermYN="N" IsPermutedTermYN="N" LexicalTag="NON" RecordPreferredTermYN="N">
                  <TermUI>ger0000003</TermUI>
                  <String>Schlachthoefe</String>
                  <DateCreated>
                    <Year>2003</Year>
                    <Month>04</Month>
                    <Day>25</Day>
                  </DateCreated>
                </Term>
                <Term ConceptPreferredTermYN="N" IsPermutedTermYN="N" LexicalTag="NON" RecordPreferredTermYN="N">
                  <TermUI>ger0027610</TermUI>
                  <String>Schlachthäuser</String>
                  <DateCreated>
                    <Year>2003</Year>
                    <Month>04</Month>
                    <Day>25</Day>
                  </DateCreated>
                </Term>
                <Term ConceptPreferredTermYN="N" IsPermutedTermYN="N" LexicalTag="NON" RecordPreferredTermYN="N">
                  <TermUI>ger0027610</TermUI>
                  <String>Schlachthaeuser</String>
                  <DateCreated>
                    <Year>2003</Year>
                    <Month>04</Month>
                    <Day>25</Day>
                  </DateCreated>
                </Term>
              </TermList>
            </Concept>
          </ConceptList>
        </DescriptorRecord>
    """
    mesh = {
        "record": mesh_descriptor,
    }
    mesh_entry = StreamEntry(mesh)

    transformer = MeSHSubjectXMLTransformer()
    assert expected_mesh_result == transformer.apply(mesh_entry).entry
