# coding=utf-8
# Copyright 2019 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Dictionaries that are used to validate and cross-classify tags of entries."""

import collections
import dataclasses
from typing import Dict, OrderedDict, Set, Tuple


@dataclasses.dataclass
class TagSetItem:
  tag: str = dataclasses.field(default=None)
  output_as: str = dataclasses.field(default=None)
  formatting: str = dataclasses.field(default="lower")
  is_fst_state: bool = dataclasses.field(default=True)
  cross_classify_as: Tuple = dataclasses.field(default_factory=tuple)
  required_features: OrderedDict[str, Set] = dataclasses.field(
      default_factory=collections.OrderedDict)
  optional_features: Dict[str, Set] = dataclasses.field(default_factory=dict)


_TAG_SET = (
    # ADJ: Adjective.
    TagSetItem(tag="JJ",
               cross_classify_as=("NN", "NOMP", "PRI", "RB"),
               optional_features={
                   "Emphasis": {"True"},
               }),
    TagSetItem(tag="JJN",
               is_fst_state=False,
               cross_classify_as=("JJ", "NN", "NOMP"),
               optional_features={
                   "Emphasis": {"True"},
               }),
    # ADP: Adposition.
    TagSetItem(tag="IN",
               cross_classify_as=("NN", "NOMP"),
               required_features=collections.OrderedDict([
                   ("ComplementType", {
                       "CAbl", "CAcc", "CBare", "CDat", "CFin", "CGen", "CIns",
                       "CNum"
                   }),
               ])),
    # ADV: Adverb.
    TagSetItem(tag="RB",
               optional_features={
                   "Emphasis": {"True"},
                   "Temporal": {"True"},
               }),
    TagSetItem(tag="RB-TEMP",
               output_as="RB",
               cross_classify_as=("NN-TEMP", "NOMP"),
               required_features=collections.OrderedDict([
                   ("Temporal", {"True"}),
               ])),
    TagSetItem(tag="WRB", cross_classify_as=("NOMP",)),
    # AFFIX: Affix.
    TagSetItem(tag="PFX"),
    # CONJ: Conjunction.
    TagSetItem(tag="CC",
               required_features=collections.OrderedDict([
                   ("ConjunctionType", {"Adv", "Coor", "Par", "Sub"}),
               ])),
    # DET: Determiner.
    TagSetItem(tag="DT",
               cross_classify_as=("NOMP", "PRI"),
               required_features=collections.OrderedDict([
                   ("DeterminerType", {"Def", "Dem", "Dir", "Ind"}),
               ])),
    TagSetItem(tag="PDT", cross_classify_as=("NOMP",)),
    TagSetItem(tag="WDT", cross_classify_as=("PRI", "NOMP")),
    # EXS: Existential.
    TagSetItem(tag="EX", cross_classify_as=("NOMP-CASE-BARE",)),
    # NOUN: Noun.
    TagSetItem(tag="ADD", cross_classify_as=("NOMP-WITH-APOS",)),
    TagSetItem(tag="NN", cross_classify_as=("NOMP",)),
    TagSetItem(tag="NN-ABBR",
               output_as="NN",
               formatting="upper",
               cross_classify_as=("NOMP-WITH-APOS",)),
    TagSetItem(tag="NN-ABBR-APOS",
               output_as="NN",
               formatting="upper",
               cross_classify_as=("NOMP-APOS",)),
    TagSetItem(tag="NN-TEMP",
               output_as="NN",
               required_features=collections.OrderedDict([
                   ("Temporal", {"True"}),
               ])),
    TagSetItem(tag="NNP",
               formatting="capitals",
               cross_classify_as=("NOMP-WITH-APOS",)),
    TagSetItem(tag="NNP-ABBR",
               output_as="NNP",
               formatting="upper",
               cross_classify_as=("NOMP-WITH-APOS",)),
    # NUM: Number.
    TagSetItem(tag="CD", cross_classify_as=("NN", "NOMP-WITH-APOS")),
    TagSetItem(tag="CD-DIST",
               is_fst_state=False,
               cross_classify_as=("NN", "NOMP-WITH-APOS")),
    TagSetItem(tag="CD-ORD",
               is_fst_state=False,
               cross_classify_as=("NN", "NOMP-WITH-APOS")),
    # ONOM: Onomatopoeic.
    TagSetItem(tag="DUP"),
    # PRON: Pronoun.
    TagSetItem(tag="PRD", cross_classify_as=("NOMP",)),
    TagSetItem(tag="PRD-PNON",
               output_as="PRD",
               cross_classify_as=("NOMP-PNON",),
               required_features=collections.OrderedDict([
                   ("PersonNumber",
                    {"A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl"}),
                   ("Possessive", {"Pnon"}),
               ])),
    TagSetItem(tag="PRD-PNPOSS",
               output_as="PRD",
               cross_classify_as=("NOMP-PNPOSS",),
               required_features=collections.OrderedDict([
                   ("PersonNumber",
                    {"A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl"}),
               ])),
    TagSetItem(tag="PRI", cross_classify_as=("NOMP",)),
    TagSetItem(tag="PRP",
               cross_classify_as=("NOMP-PN",),
               required_features=collections.OrderedDict([
                   ("PersonNumber",
                    {"A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl"}),
               ])),
    TagSetItem(tag="PRP-CASE",
               output_as="PRP",
               cross_classify_as=("NOMP-CASE-MARKED",),
               required_features=collections.OrderedDict([
                   ("PersonNumber",
                    {"A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl"}),
                   ("Possessive", {"Pnon"}),
                   ("Case", {"Acc", "Abl", "Dat", "Gen", "Ins", "Loc"}),
               ])),
    TagSetItem(tag="PRP-IRR",
               output_as="PRP",
               cross_classify_as=("NOMP-PNON",),
               required_features=collections.OrderedDict([
                   ("PersonNumber",
                    {"A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl"}),
                   ("Possessive", {"Pnon"}),
               ])),
    TagSetItem(tag="PRP$",
               cross_classify_as=("NOMP-PNON",),
               required_features=collections.OrderedDict([
                   ("PersonNumber",
                    {"A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl"}),
                   ("Possessive", {"Pnon"}),
               ])),
    TagSetItem(tag="PRR", cross_classify_as=("NOMP",)),
    TagSetItem(tag="WP", cross_classify_as=("NOMP",)),
    # PRT: Particle.
    TagSetItem(tag="EP"),
    TagSetItem(tag="OP"),
    TagSetItem(tag="RPC"),
    TagSetItem(tag="RPNEG", cross_classify_as=("NOMP-CASE-BARE",)),
    TagSetItem(tag="RPQ", cross_classify_as=("NOMP-CASE-BARE",)),
    # PUNCT: Punctuation.
    TagSetItem(tag="PUNCT-1", output_as="."),
    TagSetItem(tag="PUNCT-2", output_as=","),
    TagSetItem(tag="PUNCT-3", output_as=":"),
    TagSetItem(tag="PUNCT-4", output_as="("),
    TagSetItem(tag="PUNCT-5", output_as=")"),
    TagSetItem(tag="PUNCT-6", output_as="``"),
    TagSetItem(tag="PUNCT-7", output_as="'"),
    TagSetItem(tag="PUNCT-8", output_as="-"),
    # VERB: Verb.
    TagSetItem(tag="NOMP"),
    TagSetItem(tag="NOMP-APOS", output_as="NOMP"),
    TagSetItem(tag="NOMP-CASE-BARE",
               output_as="NOMP",
               required_features=collections.OrderedDict([
                   ("PersonNumber", {"A3sg"}),
                   ("Possessive", {"Pnon"}),
                   ("Case", {"Bare"}),
               ])),
    TagSetItem(tag="NOMP-CASE-MARKED",
               output_as="NOMP",
               required_features=collections.OrderedDict([
                   ("PersonNumber",
                    {"A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl"}),
                   ("Possessive", {"Pnon"}),
                   ("Case", {"Acc", "Abl", "Dat", "Gen", "Ins", "Loc"}),
               ])),
    TagSetItem(tag="NOMP-PN",
               output_as="NOMP",
               required_features=collections.OrderedDict([
                   ("PersonNumber",
                    {"A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl"}),
               ])),
    TagSetItem(tag="NOMP-PNON",
               output_as="NOMP",
               required_features=collections.OrderedDict([
                   ("PersonNumber",
                    {"A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl"}),
                   ("Possessive", {"Pnon"}),
               ])),
    TagSetItem(tag="NOMP-PNPOSS",
               output_as="NOMP",
               required_features=collections.OrderedDict([
                   ("PersonNumber",
                    {"A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl"}),
               ])),
    TagSetItem(tag="NOMP-WITH-APOS", output_as="NOMP"),
    TagSetItem(tag="VB-HL-AR-DHR", output_as="VB"),
    TagSetItem(tag="VB-HL-AR-HR", output_as="VB"),
    TagSetItem(tag="VB-HL-AR-HT", output_as="VB"),
    TagSetItem(tag="VB-HL-AR-NO", output_as="VB"),
    TagSetItem(tag="VB-HL-AR-T", output_as="VB"),
    TagSetItem(tag="VB-HL-HR-DHR", output_as="VB"),
    TagSetItem(tag="VB-HL-HR-NO", output_as="VB"),
    TagSetItem(tag="VB-HL-HR-T", output_as="VB"),
    TagSetItem(tag="VB-HN-AR-DHR", output_as="VB"),
    TagSetItem(tag="VB-HN-HR-DHR", output_as="VB"),
    TagSetItem(tag="VB-HN-HR-NO", output_as="VB"),
    TagSetItem(tag="VB-HN-HR-T", output_as="VB"),
    TagSetItem(tag="VB-ON-OR-DHR", output_as="VB"),
    TagSetItem(tag="VB-ON-OR-T", output_as="VB"),
    # X: Other.
    TagSetItem(tag="FW"),
    TagSetItem(tag="GW"),
    TagSetItem(tag="LS"),
    TagSetItem(tag="NFP"),
    TagSetItem(tag="SYM"),
    TagSetItem(tag="UH"),
    TagSetItem(tag="XX"),
)

# Set of valid part-of-speech tags that can be encountered as the value of the
# 'tag' field of valid lexicon entries.
VALID_TAGS = {t.tag for t in _TAG_SET}

# Map of annotated part-of-speech tags to output part-of-speech tags. Output
# tags are displayed in the morphological analysis strings that are generated
# by the compiled FST for an input word.
OUTPUT_AS = {t.tag: t.output_as if t.output_as else t.tag for t in _TAG_SET}

# Map of part-of-speech tags to a specifier which defines how the root forms
# should be formatted in the output morphological analysis strings. Values
# could only  be 'lower' (for lowercase root forms, e.g. common nouns), 'upper'
# (for uppercase root forms, e.g. abbreviations), or 'capitals' (for
# capitalized root forms, e.g. proper nouns).
FORMATTING = {t.tag: t.formatting for t in _TAG_SET}

# Set of part-of-speech tags that can be used as a state name in the compiled
# morphotactics FST. If a part-of-speech tag is in VALID_TAGS set but not in
# FST_STATES set, then it is only used for lexicon annotation purposes. Lexicon
# entries that are annotated with those tags are cross-classified to other
# parts of speech that are in FST_STATES set.
FST_STATES = {t.tag for t in _TAG_SET if t.is_fst_state}

# Map of part-of-speech cross-classification pairs. Lexicon entries whose tag
# is a key of this dictionary are cross-classified to the parts of speech that
# are in the respective tuple of values. Cross-classifying a lexicon entry
# means adding an additional new identical entry to the lexicon by only
# rewriting the tag of the original entry.
CROSS_CLASSIFY_AS = {t.tag: t.cross_classify_as for t in _TAG_SET}

# Map of part-of-speech tags to an ordered dictionary of required feature
# category-value pairs. Lexicon entries whose tag is a key of this dictionary
# are expected to be annotated with the corresponding set of features in order
# to be valid. Values of this dictionary contain the feature category-value
# pairs in the order they are expected to appear in the annotations.
REQUIRED_FEATURES = {t.tag: t.required_features for t in _TAG_SET}

# Map of part-of-speech tags to a dictionary of optional feature category-value
# pairs. Lexicon entries whose tag is a key of this dictionary can optionally
# be annotated with one of the feature category-value pairs in the
# corresponding dicionary of optional features.
OPTIONAL_FEATURES = {t.tag: t.optional_features for t in _TAG_SET}
