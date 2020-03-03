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
"""Tests for src.analyzer.morphotactics.model_compile."""

import os
import shutil
import subprocess

from absl.testing import absltest
from absl.testing import parameterized

_LEX_DIR = os.path.join("src", "analyzer", "lexicon", "testdata")
_MORPH_DIR = os.path.join("src", "analyzer", "morphotactics", "testdata")

_EXPECTED_SYMBOLS = os.path.join(_MORPH_DIR, "complex_symbols_expected.txt")
_EXPECTED_FST = os.path.join(_MORPH_DIR, "text_fst_expected.txt")

_TMP_DIR = "tmp"
_TMP_LEX_DIR = os.path.join(_TMP_DIR, "lexicon")
_TMP_MORPH_DIR = os.path.join(_TMP_DIR, "morphotactics")
_TMP_OUT_DIR = os.path.join(_TMP_DIR, "output")


def _read_file(path):
  with open(path, "r", encoding="utf-8") as f:
    read = f.read()
  return read


def _copy_files(filenames, source_directory, destination_directory):
  for filename in filenames:
    from_ = os.path.join(source_directory, filename)
    to = os.path.join(destination_directory, filename)
    shutil.copyfile(from_, to)


class MainTest(parameterized.TestCase):

  def setUp(self):
    super(MainTest, self).setUp()
    for tmp_directory in [_TMP_LEX_DIR, _TMP_MORPH_DIR]:
      os.makedirs(tmp_directory)

  def tearDown(self):
    super(MainTest, self).tearDown()
    for tmp_directory in [_TMP_LEX_DIR, _TMP_MORPH_DIR, _TMP_OUT_DIR]:
      if os.path.exists(tmp_directory):
        shutil.rmtree(tmp_directory)

  def _test_call(self, lexicon_dir, morphotactics_dir, output_dir):
    subprocess.check_call([
        "src/analyzer/morphotactics/model_compile",
        "--lexicon_dir=%s" % lexicon_dir,
        "--morphotactics_dir=%s" % morphotactics_dir,
        "--output_dir=%s" % output_dir,
    ])

  def _test_call_success(self, lexicon_dir, morphotactics_dir, output_dir):
    self._test_call(lexicon_dir, morphotactics_dir, output_dir)

    actual_symbols = os.path.join(output_dir, "complex_symbols.syms")
    self.assertTrue(os.path.isfile(actual_symbols))
    self.assertEqual(_read_file(_EXPECTED_SYMBOLS), _read_file(actual_symbols))

    actual_fst = os.path.join(output_dir, "morphotactics.txt")
    self.assertTrue(os.path.isfile(actual_fst))
    self.assertEqual(_read_file(_EXPECTED_FST), _read_file(actual_fst))

  def _test_call_failure(self, lexicon_dir, morphotactics_dir, output_dir):
    with self.assertRaises(subprocess.CalledProcessError):
      self._test_call(lexicon_dir, morphotactics_dir, output_dir)

    actual_symbols = os.path.join(output_dir, "complex_symbols.syms")
    self.assertFalse(os.path.isfile(actual_symbols))

    actual_fst = os.path.join(output_dir, "morphotactics.txt")
    self.assertFalse(os.path.isfile(actual_fst))

  def test_success_on_valid_lexicon_and_morphotactics(self):
    lexicons = [
        "valid_entries_1.tsv",
        "valid_entries_2.tsv",
    ]
    morphotactics = [
        "morphotactics_valid_rules_1.txt",
        "morphotactics_valid_rules_2.txt",
    ]
    _copy_files(lexicons, _LEX_DIR, _TMP_LEX_DIR)
    _copy_files(morphotactics, _MORPH_DIR, _TMP_MORPH_DIR)
    self._test_call_success(_TMP_LEX_DIR, _TMP_MORPH_DIR, _TMP_OUT_DIR)

  @parameterized.named_parameters([
      {
          "testcase_name": "EmptyLexicon",
          "lexicon": "invalid_empty_lexicon.tsv",
      },
      {
          "testcase_name": "OnlyHeader",
          "lexicon": "invalid_only_header.tsv",
      },
      {
          "testcase_name": "OnlyEmptyRowsWithHeader",
          "lexicon": "invalid_only_empty_rows.tsv",
      },
      {
          "testcase_name": "MissingTagField",
          "lexicon": "invalid_missing_tag_field.tsv",
      },
      {
          "testcase_name": "MissingRootField",
          "lexicon": "invalid_missing_root_field.tsv",
      },
      {
          "testcase_name": "MissingMorphophonemicsField",
          "lexicon": "invalid_missing_morphophonemics_field.tsv",
      },
      {
          "testcase_name": "MissingFeaturesField",
          "lexicon": "invalid_missing_features_field.tsv",
      },
      {
          "testcase_name": "MissingIsCompoundField",
          "lexicon": "invalid_missing_is_compound_field.tsv",
      },
      {
          "testcase_name": "EmptyTagValue",
          "lexicon": "invalid_empty_tag_value.tsv",
      },
      {
          "testcase_name": "EmptyRootValue",
          "lexicon": "invalid_empty_root_value.tsv",
      },
      {
          "testcase_name": "EmptyMorphophonemicsValue",
          "lexicon": "invalid_empty_morphophonemics_value.tsv",
      },
      {
          "testcase_name": "EmptyFeaturesValue",
          "lexicon": "invalid_empty_features_value.tsv",
      },
      {
          "testcase_name": "EmptyIsCompoundValue",
          "lexicon": "invalid_empty_is_compound_value.tsv",
      },
      {
          "testcase_name": "WhitespaceInTagValue",
          "lexicon": "invalid_whitespace_in_tag_value.tsv",
      },
      {
          "testcase_name": "WhitespaceInMorphophonemicsValue",
          "lexicon": "invalid_whitespace_in_morphophonemics_value.tsv",
      },
      {
          "testcase_name": "WhitespaceInFeaturesValue",
          "lexicon": "invalid_whitespace_in_features_value.tsv",
      },
      {
          "testcase_name": "InvalidTagValue",
          "lexicon": "invalid_tag_value.tsv",
      },
      {
          "testcase_name": "InvalidIsCompoundValue",
          "lexicon": "invalid_is_compound_value.tsv",
      },
      {
          "testcase_name": "InvalidMorphophonemicsValue",
          "lexicon": "invalid_morphophonemics_value.tsv",
      },
      {
          "testcase_name": "InvalidFeaturesValue",
          "lexicon": "invalid_features_value.tsv",
      },
      {
          "testcase_name": "MissingRequiredFeatures",
          "lexicon": "invalid_missing_required_features.tsv",
      },
      {
          "testcase_name": "InvalidRequiredFeatures",
          "lexicon": "invalid_required_features.tsv",
      },
      {
          "testcase_name": "InvalidOptionalFeatures",
          "lexicon": "invalid_optional_features.tsv",
      },
      {
          "testcase_name": "InvalidRedundantFeatures",
          "lexicon": "invalid_redundant_features.tsv",
      },
  ])
  def test_raises_exception_on_source_lexicon(self, lexicon):
    morphotactics = [
        "morphotactics_valid_rules_1.txt",
        "morphotactics_valid_rules_2.txt",
    ]
    _copy_files(morphotactics, _MORPH_DIR, _TMP_MORPH_DIR)
    _copy_files([lexicon], _LEX_DIR, _TMP_LEX_DIR)
    self._test_call_failure(_TMP_LEX_DIR, _TMP_MORPH_DIR, _TMP_OUT_DIR)

  @parameterized.named_parameters([
      {
          "testcase_name": "EmptyMorphotactics",
          "morphotactics": "morphotactics_invalid_empty.txt",
      },
      {
          "testcase_name": "OnlyComments",
          "morphotactics": "morphotactics_invalid_only_comments.txt",
      },
      {
          "testcase_name": "OnlyEmptyLines",
          "morphotactics": "morphotactics_invalid_only_empty_lines.txt",
      },
      {
          "testcase_name": "InvalidNumberOfRuleTokens",
          "morphotactics": "morphotactics_invalid_number_of_tokens.txt",
      },
      {
          "testcase_name": "InvalidRuleInputToken",
          "morphotactics": "morphotactics_invalid_rule_input.txt",
      },
      {
          "testcase_name": "InvalidRuleOutputToken",
          "morphotactics": "morphotactics_invalid_rule_output.txt",
      },
  ])
  def test_raises_exception_on_source_morphotactics(self, morphotactics):
    lexicons = [
        "valid_entries_1.tsv",
        "valid_entries_2.tsv",
    ]
    _copy_files(lexicons, _LEX_DIR, _TMP_LEX_DIR)
    _copy_files([morphotactics], _MORPH_DIR, _TMP_MORPH_DIR)
    self._test_call_failure(_TMP_LEX_DIR, _TMP_MORPH_DIR, _TMP_OUT_DIR)

  @parameterized.named_parameters([
      {
          "testcase_name": "EmptyLexiconDirectoryPath",
          "lexicon_dir": "",
      },
      {
          "testcase_name": "InvalidLexiconDirectoryPath",
          "lexicon_dir": "invalid_dir_path",
      },
      {
          "testcase_name": "EmptyMorphotacticsDirectoryPath",
          "morphotactics_dir": "",
      },
      {
          "testcase_name": "InvalidMorphotacticsDirectoryPath",
          "morphotactics_dir": "invalid_dir_path",
      },
  ])
  def test_raises_exception_on_argument(self,
                                        lexicon_dir=_TMP_LEX_DIR,
                                        morphotactics_dir=_TMP_MORPH_DIR,
                                        output_dir=_TMP_OUT_DIR):
    self._test_call_failure(lexicon_dir, morphotactics_dir, output_dir)


if __name__ == "__main__":
  absltest.main()
