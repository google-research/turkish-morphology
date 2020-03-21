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

"""Functions to validate structural well-formedness of analysis protobufs."""

from typing import Optional

from turkish_morphology import analysis_pb2

_Affix = analysis_pb2.Affix
_Analysis = analysis_pb2.Analysis
_Feature = analysis_pb2.Feature
_Ig = analysis_pb2.InflectionalGroup
_Root = analysis_pb2.Root


class IllformedAnalysisError(Exception):
  """Raised when a human-readable analysis is structurally ill-formed."""


def _root(root: _Root) -> None:
  """Checks if root is structurally well-formed.

  Args:
    root: root analysis.

  Raises:
    IllformedAnalysisError: root is missing the morpheme field, or its
      morpheme field is set as empty string.
  """
  if not root.HasField("morpheme"):
    raise IllformedAnalysisError(f"Root is missing morpheme: '{root}'")

  if not root.morpheme:
    raise IllformedAnalysisError(f"Root morpheme is empty: '{root}'")


def _feature(feature: _Feature) -> None:
  """Checks if feature is structurally well-formed.

  Args:
    feature: morphological analysis feature.

  Raises:
    IllformedAnalysisError: feature is missing category or value field, or
      its category or value field is set as empty string.
  """
  if not feature.HasField("category"):
    raise IllformedAnalysisError(f"Feature is missing category: '{feature}'")

  if not feature.category:
    raise IllformedAnalysisError(f"Feature category is empty: '{feature}'")

  if not feature.HasField("value"):
    raise IllformedAnalysisError(f"Feature is missing value: '{feature}'")

  if not feature.value:
    raise IllformedAnalysisError(f"Feature value is empty: '{feature}'")


def _affix(affix: _Affix, derivational: Optional[bool] = False) -> None:
  """Checks if affix is structurally well-formed.

  Args:
    affix: affix analysis.
    derivational: if True, affix corresponds to a derivational feature.

  Raises:
    IllformedAnalysisError: affix is missing the feature field, or affix is
      derivational but its meta_morpheme field is missing or its meta_morpheme
      field is set as empty string.
  """
  if not affix.HasField("feature"):
    raise IllformedAnalysisError(f"Affix is missing feature: '{affix}'")

  _feature(affix.feature)

  if not derivational:
    return

  if not affix.HasField("meta_morpheme"):
    raise IllformedAnalysisError(
        f"Derivational affix is missing meta-morpheme: '{affix}'")

  if not affix.meta_morpheme:
    raise IllformedAnalysisError(
        f"Derivational affix meta-morpheme is empty: '{affix}'")


def _inflectional_group(ig: _Ig, position: int) -> None:
  """Checks if inflectional group is structurally well-formed.

  Args:
    ig: inflectional group analysis.
    position: index of the inflectional group w.r.t. the array of inflectional
      groups of the morphological analysis it belongs to.

  Raises:
    IllformedAnalysisError: inflectional group is missing part-of-speech tag,
      or its part-of-speech tag is set as empty string, or inflectional group
      is the first in morphological analysis and it is missing the root field,
      or inflectional group is derived and it is missing the derivation field.
  """
  if not ig.HasField("pos"):
    raise IllformedAnalysisError(
        f"Inflectional group {position + 1} is missing part-of-speech tag:"
        f" '{ig}'")

  if not ig.pos:
    raise IllformedAnalysisError(
        f"Inflectional group {position + 1} part-of-speech tag is empty:"
        f" '{ig}'")

  if position == 0:
    if not ig.HasField("root"):
      raise IllformedAnalysisError(
          f"Inflectional group {position + 1} is missing root: '{ig}'")

    _root(ig.root)
  else:
    if not ig.HasField("derivation"):
      raise IllformedAnalysisError(
          f"Inflectional group {position + 1} is missing derivational affix:"
          f" '{ig}'")

    _affix(ig.derivation, derivational=True)

  for inflection in ig.inflection:
    _affix(inflection)


def analysis(analysis: _Analysis) -> None:
  """Checks if analysis protobuf is structurally well-formed.

  Args:
    analysis: morphological analysis.

  Raises:
    IllformedAnalysisError: analysis is missing inflectional groups.
  """
  if not analysis.ig:
    raise IllformedAnalysisError(
        "Analysis is missing inflectional groups: 'analysis'")

  for position, ig in enumerate(analysis.ig):
    _inflectional_group(ig, position)
