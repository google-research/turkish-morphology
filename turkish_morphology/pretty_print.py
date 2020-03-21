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

"""Functions to print human-readable analyses from analysis protobufs."""

from typing import Optional

from turkish_morphology import analysis_pb2

_Affix = analysis_pb2.Affix
_Analysis = analysis_pb2.Analysis
_Feature = analysis_pb2.Feature
_Ig = analysis_pb2.InflectionalGroup
_Root = analysis_pb2.Root


def _root(root: _Root) -> str:
  """Formats root analysis.

  Args:
    root: root analysis.

  Returns:
    Human-readable string that is used to represent the morpheme of the root
    analysis (e.g. "araba").
  """
  morpheme = root.morpheme
  return f"{morpheme}"


def _feature(feature: _Feature) -> str:
  """Formats morphological analysis feature.

  Args:
    feature: morphological analysis feature.

  Returns:
    Human-readable string that is used to represent the morphological analysis
    feature (e.g. '[Case=Abl]').
  """
  category = feature.category
  value = feature.value
  return f"[{category}={value}]"


def _affix(affix: _Affix, derivational: Optional[bool] = False) -> str:
  """Formats affix analysis.

  Args:
    affix: affix analysis.
    derivational: if True, affix corresponds to a derivational feature.

  Returns:
    Human-readable string that is used to represent the affix analysis (e.g.
    '+lAr[PersonNumber=A3pl]').
  """
  delimiter = "-" if derivational else "+"
  meta_morpheme = affix.meta_morpheme
  feature = _feature(affix.feature)
  return f"{delimiter}{meta_morpheme}{feature}"


def _inflectional_group(ig: _Ig, position: int) -> str:
  """Formats inflectional group analysis.

  Args:
    ig: inflectional group analysis.
    position: index of the inflectional group w.r.t. the array of inflectional
      groups of the morphological analysis it belongs to.

  Returns:
    Human-readable string that is used to represent the inflectional group
    analysis (e.g. '(araba[NN]+lAr[PersonNumber=A3pl]+[Possessive=Pnon]
    +DA[Case=Loc])').
  """
  pos = f"[{ig.pos}]"

  if position == 0:
    root = _root(ig.root)
    pos_root_derivation = f"{root}{pos}"
  else:
    derivation = _affix(ig.derivation, derivational=True)
    pos_root_derivation = f"{pos}{derivation}"

  inflections = "".join(_affix(i) for i in ig.inflection)

  if ig.HasField("proper"):
    proper = "+[Proper=True]" if ig.proper else "+[Proper=False]"
  else:
    proper = ""

  return f"({pos_root_derivation}{inflections}){proper}"


def analysis(analysis: _Analysis) -> str:
  """Constructs human-readable analysis from analysis protobuf.

  Args:
    analysis: morphological analysis.

  Returns:
    Human-readable string that is used to represent the morphological analysis
    (e.g. '(araba[NN]+lAr[PersonNumber=A3pl]+[Possessive=Pnon]+DA[Case=Loc])
    +[Proper=True]').
  """
  return "".join(_inflectional_group(ig, i) for i, ig in enumerate(analysis.ig))
