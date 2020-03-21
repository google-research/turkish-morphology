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

"""Tests for turkish_morphology.validate."""

import os

from turkish_morphology import analysis_pb2
from turkish_morphology import validate

from absl.testing import absltest
from absl.testing import parameterized
from google.protobuf import text_format

_TESTDATA_DIR = "turkish_morphology/testdata"


def _read_file(path):
  with open(path, "r") as f:
    read = f.read()
  return read


def _read_analysis(basename):
  path = os.path.join(_TESTDATA_DIR, f"{basename}.pbtxt")
  return text_format.Parse(_read_file(path), analysis_pb2.Analysis())


class AnalysisTest(parameterized.TestCase):

  @parameterized.named_parameters([
      {
          "testcase_name": "SingleInflectionalGroupsWithProperFeature",
          "basename": "araba_with_proper",
      },
      {
          "testcase_name": "SingleInflectionalGroupsWithoutProperFeature",
          "basename": "araba_without_proper",
      },
      {
          "testcase_name": "MultipleInflectionalGroupsWithProperFeature",
          "basename": "yasa_with_proper",
      },
      {
          "testcase_name": "MultipleInflectionalGroupsWithoutProperFeature",
          "basename": "yasa_without_proper",
      },
  ])
  def test_success(self, basename):
    analysis = _read_analysis(basename)
    actual = validate.analysis(analysis)
    self.assertIsNone(actual)

  @parameterized.named_parameters([
      {
          "testcase_name": "AnalysisMissingInflectionalGroups",
          "basename": "invalid_empty_analysis",
          "message": "Analysis is missing inflectional groups",
      },
      {
          "testcase_name": "InflectionalGroupMissingPartOfSpeechTag",
          "basename": "invalid_ig_missing_pos",
          "message": "Inflectional group 2 is missing part-of-speech tag",
      },
      {
          "testcase_name": "InflectionalGroupEmptyPartOfSpeechTag",
          "basename": "invalid_ig_empty_pos",
          "message": "Inflectional group 2 part-of-speech tag is empty",
      },
      {
          "testcase_name": "FirstInflectionalGroupMissingRoot",
          "basename": "invalid_first_ig_missing_root",
          "message": "Inflectional group 1 is missing root",
      },
      {
          "testcase_name": "DerivedInflectionalGroupMissingDerivation",
          "basename": "invalid_derived_ig_missing_derivation",
          "message": "Inflectional group 2 is missing derivational affix",
      },
      {
          "testcase_name": "AffixMissingFeature",
          "basename": "invalid_affix_missing_feature",
          "message": "Affix is missing feature",
      },
      {
          "testcase_name": "DerivationalAffixMissingMetaMorpheme",
          "basename": "invalid_derivational_affix_missing_meta_morpheme",
          "message": "Derivational affix is missing meta-morpheme",
      },
      {
          "testcase_name": "DerivationalAffixEmptyMetaMorpheme",
          "basename": "invalid_derivational_affix_empty_meta_morpheme",
          "message": "Derivational affix meta-morpheme is empty",
      },
      {
          "testcase_name": "FeatureMissingCategory",
          "basename": "invalid_feature_missing_category",
          "message": "Feature is missing category",
      },
      {
          "testcase_name": "FeatureEmptyCategory",
          "basename": "invalid_feature_empty_category",
          "message": "Feature category is empty",
      },
      {
          "testcase_name": "FeatureMissingValue",
          "basename": "invalid_feature_missing_value",
          "message": "Feature is missing value",
      },
      {
          "testcase_name": "FeatureEmptyValue",
          "basename": "invalid_feature_empty_value",
          "message": "Feature value is empty",
      },
      {
          "testcase_name": "RootMissingMorpheme",
          "basename": "invalid_root_missing_morpheme",
          "message": "Root is missing morpheme",
      },
      {
          "testcase_name": "RootEmptyMorpheme",
          "basename": "invalid_root_empty_morpheme",
          "message": "Root morpheme is empty",
      },
  ])
  def test_raises_exception(self, basename, message):
    analysis = _read_analysis(basename)

    with self.assertRaisesRegexp(validate.IllformedAnalysisError, message):
      validate.analysis(analysis)


if __name__ == "__main__":
  absltest.main()
