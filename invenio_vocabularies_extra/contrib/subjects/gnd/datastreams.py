# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 University of Münster.
#
# invenio-vocabularies-extra is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom datastream transformer for GND subjects."""
import lxml.etree as ET
from invenio_access.permissions import system_identity
from invenio_vocabularies.contrib.subjects.datastreams import SubjectsServiceWriter
from invenio_vocabularies.datastreams.transformers import BaseTransformer

ISO639_1_TO_2 = {
    "aar": "aa",
    "abk": "ab",
    "afr": "af",
    "aka": "ak",
    "alb": "sq",
    "amh": "am",
    "ara": "ar",
    "arg": "an",
    "arm": "hy",
    "asm": "as",
    "ava": "av",
    "ave": "ae",
    "aym": "ay",
    "aze": "az",
    "bak": "ba",
    "bam": "bm",
    "baq": "eu",
    "bel": "be",
    "ben": "bn",
    "bih": "bh",
    "bis": "bi",
    "bos": "bs",
    "bre": "br",
    "bul": "bg",
    "bur": "my",
    "cat": "ca",
    "cha": "ch",
    "che": "ce",
    "chi": "zh",
    "chu": "cu",
    "chv": "cv",
    "cor": "kw",
    "cos": "co",
    "cre": "cr",
    "cze": "cs",
    "dan": "da",
    "div": "dv",
    "dut": "nl",
    "dzo": "dz",
    "eng": "en",
    "epo": "eo",
    "est": "et",
    "ewe": "ee",
    "fao": "fo",
    "fij": "fj",
    "fin": "fi",
    "fre": "fr",
    "fry": "fy",
    "ful": "ff",
    "geo": "ka",
    "ger": "de",
    "gla": "gd",
    "gle": "ga",
    "glg": "gl",
    "glv": "gv",
    "gre": "el",
    "grn": "gn",
    "guj": "gu",
    "hat": "ht",
    "hau": "ha",
    "heb": "he",
    "her": "hz",
    "hin": "hi",
    "hmo": "ho",
    "hrv": "hr",
    "hun": "hu",
    "ibo": "ig",
    "ice": "is",
    "ido": "io",
    "iii": "ii",
    "iku": "iu",
    "ile": "ie",
    "ina": "ia",
    "ind": "id",
    "ipk": "ik",
    "ita": "it",
    "jav": "jv",
    "jpn": "ja",
    "kal": "kl",
    "kan": "kn",
    "kas": "ks",
    "kau": "kr",
    "kaz": "kk",
    "khm": "km",
    "kik": "ki",
    "kin": "rw",
    "kir": "ky",
    "kom": "kv",
    "kon": "kg",
    "kor": "ko",
    "kua": "kj",
    "kur": "ku",
    "lao": "lo",
    "lat": "la",
    "lav": "lv",
    "lim": "li",
    "lin": "ln",
    "lit": "lt",
    "ltz": "lb",
    "lub": "lu",
    "lug": "lg",
    "mac": "mk",
    "mah": "mh",
    "mal": "ml",
    "mao": "mi",
    "mar": "mr",
    "may": "ms",
    "mlg": "mg",
    "mlt": "mt",
    "mon": "mn",
    "nau": "na",
    "nav": "nv",
    "nbl": "nr",
    "nde": "nd",
    "ndo": "ng",
    "nep": "ne",
    "nno": "nn",
    "nob": "nb",
    "nor": "no",
    "nya": "ny",
    "oci": "oc",
    "oji": "oj",
    "ori": "or",
    "orm": "om",
    "oss": "os",
    "pan": "pa",
    "per": "fa",
    "pli": "pi",
    "pol": "pl",
    "por": "pt",
    "pus": "ps",
    "que": "qu",
    "roh": "rm",
    "rum": "ro",
    "run": "rn",
    "rus": "ru",
    "sag": "sg",
    "san": "sa",
    "sin": "si",
    "slo": "sk",
    "slv": "sl",
    "sme": "se",
    "smo": "sm",
    "sna": "sn",
    "snd": "sd",
    "som": "so",
    "sot": "st",
    "spa": "es",
    "srd": "sc",
    "srp": "sr",
    "ssw": "ss",
    "sun": "su",
    "swa": "sw",
    "swe": "sv",
    "tah": "ty",
    "tam": "ta",
    "tat": "tt",
    "tel": "te",
    "tgk": "tg",
    "tgl": "tl",
    "tha": "th",
    "tib": "bo",
    "tir": "ti",
    "ton": "to",
    "tsn": "tn",
    "tso": "ts",
    "tuk": "tk",
    "tur": "tr",
    "twi": "tw",
    "uig": "ug",
    "ukr": "uk",
    "urd": "ur",
    "uzb": "uz",
    "ven": "ve",
    "vie": "vi",
    "vol": "vo",
    "wel": "cy",
    "wln": "wa",
    "wol": "wo",
    "xho": "xh",
    "yid": "yi",
    "yor": "yo",
    "zha": "za",
    "zul": "zu",
}


class GNDMarc21Transformer(BaseTransformer):
    """Custom datastream transformer for GND subjects."""

    def apply(self, stream_entry, **kwargs):
        """
        Transform XML data to internal format.

        Input:
           A stream_entry.entry from OAIPMHHarvester is a dict with just a "record" which
           is an OAIRecord (from oaipmh_scythe).
           Record format is Marc21.

        Output:
           {
               "id": "gnd:4558957-4",
               "scheme": "GND",
               "title": {
                   "de": "Mozartjahr",
               },
               "subject": "Mozartjahr",
               "synonyms": [
                   "Mozart-Jahr",
                   "Mozart-Feier",
               ],
               "identifiers": [
                   {
                       "scheme": "url",
                       "identifier": "http://d-nb.info/gnd/4558957-4",
                   }
               ],
           }
        """
        record = ET.fromstring(stream_entry.entry["record"].get_metadata()["record"])
        xmlns = "{http://www.loc.gov/MARC21/slim}"

        result = {
            "title": {},
            "subject": "",
            "id": "",
            "scheme": "GND",
            "synonyms": [],
            "identifiers": [],
        }

        # Extracting the main ID
        datafield_024 = record.find(f"{xmlns}datafield[@tag='024']")
        if datafield_024 is not None:
            subfield_a = datafield_024.find(f"{xmlns}subfield[@code='a']")
            if subfield_a is not None:
                result["id"] = f"gnd:{subfield_a.text}"
            subfield_0 = datafield_024.find(f"{xmlns}subfield[@code='0']")
            if subfield_0 is not None:
                identifier = {
                    "scheme": "url",
                    "identifier": subfield_0.text,
                }
                result["identifiers"].append(identifier)

        # Extracting the main subject
        datafield_150 = record.find(f"{xmlns}datafield[@tag='150']")
        if datafield_150 is not None:
            subfield_a = datafield_150.find(f"{xmlns}subfield[@code='a']")
            if subfield_a is not None:
                title_de = subfield_a.text
                subfield_x = datafield_150.find(f"{xmlns}subfield[@code='x']")
                title_de = " / ".join(filter(None, [subfield_x.text, title_de]))
                subfield_g = datafield_150.find(f"{xmlns}subfield[@code='g']")
                year = "".join(filter(None, [" <", subfield_g.text, ">"]))
                if len(year) > 2:
                    title_de += year
                result["title"]["de"] = title_de
                result["subject"] = title_de

        # Adding alternative names
        datafields_750 = record.findall(f"{xmlns}datafield[@tag='750']")
        for df in datafields_750:
            subfield_4 = df.find(f"{xmlns}subfield[@code='4']")
            if subfield_4 is not None and subfield_4.text == "EQ":
                subfield_a = df.find(f"{xmlns}subfield[@code='a']")
                subfields_9 = df.findall(f"{xmlns}subfield[@code='9']")
                if subfield_a is not None:
                    lang_codes = [
                        sf.text for sf in subfields_9 if sf.text.startswith("L:")
                    ]
                    for lc in lang_codes:
                        lc = lc.replace("L:", "")
                        try:
                            two_digit_cl = ISO639_1_TO_2[lc]
                        except KeyError:
                            continue
                        else:
                            result["title"][two_digit_cl] = subfield_a.text

        # Extracting synonyms from tag 450
        datafields_450 = record.findall(f"{xmlns}datafield[@tag='450']")
        for df in datafields_450:
            subfield_a = df.find(f"{xmlns}subfield[@code='a']")
            if subfield_a is not None and subfield_a.text not in result["synonyms"]:
                synonym = subfield_a.text
                subfield_x = df.find(f"{xmlns}subfield[@code='x']")
                synonym = " / ".join(filter(None, [subfield_x.text, synonym]))
                subfield_g = df.find(f"{xmlns}subfield[@code='g']")
                year = "".join(filter(None, [" <", subfield_g.text, ">"]))
                if len(year) > 2:
                    synonym += year
                result["synonyms"].append(synonym)

        stream_entry.entry = result
        return stream_entry


VOCABULARIES_DATASTREAM_TRANSFORMERS = {
    "gnd-subjects": GNDMarc21Transformer,
}


VOCABULARIES_DATASTREAM_WRITERS = {
    "subjects-service": SubjectsServiceWriter,
}


DATASTREAM_CONFIG = {
    "readers": [
        {
            "type": "oai-pmh",
            "args": {
                "verb": "ListRecords",
                "base_url": "https://services.dnb.de/oai/repository",
                "metadata_prefix": "MARC21-xml",
                "set": "authorities:sachbegriff",
                "from": "now-10min",
                "until": "now",
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
"""gnd-subjects Data Stream configuration."""
