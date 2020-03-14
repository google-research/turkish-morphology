# coding=utf-8
# Copyright 2020 The Google Research Authors.
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

"""Functions to parse human-readable analyses into analysis protobuf messages.
"""

import re
from typing import Generator

from turkish_morphology import analysis_pb2

_Affix = analysis_pb2.Affix
_Analysis = analysis_pb2.Analysis

_AFFIX_REGEX = re.compile(
    # Derivation or inflection delimiter.
    r"[\+-]"
    # Meta-morpheme.
    r"(?P<meta_morpheme>(?:[^\W\d_]|['\.])*?)"
    # Feature category-value.
    r"\[(?P<category>[A-z]+?)=(?P<value>[A-z0-9]+?)\]")
_IG_REGEX = re.compile(
    # Beginning of an inflectional group.
    r"\("
    r"(?:"
    # Root form in first inflectional group.
    r"(?P<root>.+?)"
    # Part-of-speech tag of the first inflectional group.
    r"\[(?P<root_pos>[A-Z\.,:\(\)\'\-\"`\$]+?)\]"
    r"|"
    # Part-of-speech tag of the derived inflectional group.
    r"\[(?P<derivation_pos>[A-Z\.,:\(\)\'\-\"`\$]+?)\]"
    # Derivational morpheme and feature.
    r"(?P<derivation>-(?:[^\W\d_]|')+?\[[A-z]+?=[A-z]+?\])?"
    r")"
    # Inflectional morphemes and features.
    r"(?P<inflections>(?:\+(?:[^\W\d_]|['\.])*?\[[A-z]+?=[A-z0-9]+?\])*)"
    # End of an inflectional group.
    r"\)"
    # Optional Proper feature analysis.
    r"(?:\+\[Proper=(?P<proper>True|False)\])?")


class IllformedHumanReadableAnalysisError(Exception):
  """Raised when a human-readable analysis is structurally ill-formed."""


def _make_affix(human_readable: str) -> Generator[_Affix, None, None]:
  """Parses a sequence of human-readable affix analyses into affix protobuf.

  To illustrate, for the given human-readable analysis of below sequence of
  inflectional affixes;

      '+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]'

  this function generates the corresponding affix protobufs;

      affix {
        feature {
          category: 'PersonNumber'
          value: 'A3pl'
        }
        meta_morpheme: 'lAr'
      }
      affix {
        feature {
          category: 'Possessive'
          value: 'P1sg'
        }
        meta_morpheme: 'Hm'
      }

  Args:
    human_readable: human-readable analysis for a sequence of derivational or
      inflectional morphemes (e.g. '-DHk[Derivation=PastNom]' or
      '+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]').

  Yields:
    Affix protobuf messages that are constructed from the human-readable affix
    analyses.
  """
  matches = (m.groupdict() for m in _AFFIX_REGEX.finditer(human_readable))

  for matching in matches:
    affix = _Affix()
    affix.feature.category = matching["category"]
    affix.feature.value = matching["value"]

    if matching["meta_morpheme"]:
      affix.meta_morpheme = matching["meta_morpheme"]

    yield affix


def human_readable_analysis(human_readable: str) -> _Analysis:
  """Parses given human-readable analysis into an analysis protobuf.

  To illustrate, for the given human-readable analysis;

      '(Ali[NNP]+lAr[PersonNumber=A3pl]+[Possessive=Pnon]
      +NHn[Case=Gen])+[Proper=True]'

  this function makes the corresponding analysis protobuf;

      inflectional_group {
        pos: 'NNP'
        root {
          morpheme: 'Ali'
        }
        inflection {
          feature {
            category: 'PersonNumber'
            value: 'A3pl'
          }
          meta_morpheme: 'lAr'
        }
        inflection {
          feature {
            category: 'Possessive'
            value: 'Pnon'
          }
        }
        inflection {
          feature {
            category: 'Case'
            value: 'Gen'
          }
          meta_morpheme: 'NHn'
        }
        proper: true
      }

  For the structure of the output analysis protobufs, see:

      //turkish_morphology/analysis.proto

  Args:
    human_readable: human-readable morphological analysis.

  Raises:
    IllformedHumanReadableAnalysisError: given human-readable morphological
      analysis is structurally ill-formed (e.g. missing part-of-speech tag,
      root form, derivational/inflectional morpheme, or feature category/value,
      etc.).

  Returns:
    Analysis protobuf message that is constructed from the human-readable
    analysis.
  """
  if not human_readable:
    raise IllformedHumanReadableAnalysisError(
        "Human-readable analysis is empty.")

  igs = tuple(_IG_REGEX.finditer(human_readable))
  matches = [ig.groupdict() for ig in igs]

  if not (igs and len(human_readable) == igs[-1].end() and matches[0]["root"]
          and matches[0]["root_pos"]
          and all(m["derivation"] for m in matches[1:])
          and all(m["derivation_pos"] for m in matches[1:])):
    raise IllformedHumanReadableAnalysisError(
        f"Human-readable analysis is ill-formed: '{human_readable}'")

  analysis = _Analysis()

  for position, matching in enumerate(matches):
    ig = analysis.ig.add()

    if position == 0:
      ig.pos = matching["root_pos"]
      ig.root.morpheme = matching["root"]
    else:
      ig.pos = matching["derivation_pos"]
      derivation = tuple(_make_affix(matching["derivation"]))[0]
      ig.derivation.CopyFrom(derivation)

    inflections = _make_affix(matching["inflections"])
    ig.inflection.extend(inflections)

    if matching["proper"]:
      ig.proper = matching["proper"] == "True"

  return analysis
