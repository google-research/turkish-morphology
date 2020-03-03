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
"""Tests for src.analyzer.lexicon.validator."""

import collections

from src.analyzer.lexicon import tags
from src.analyzer.lexicon import validator

from absl.testing import absltest
from absl.testing import parameterized


def setUpModule():
  # Inject valid test tags and their expected required and optional features to
  # respective dictionaries that are used in validation. This allows us to use
  # lexicon entries that are constructed with these tags and features in below
  # test cases.
  tag_set = (
      tags._TagSetItem(tag="TAG-1"),
      tags._TagSetItem(tag="TAG-2",
                       required_features=collections.OrderedDict([
                           ("Cat1", {"Val11", "Val12"}),
                           ("Cat2", {"Val21", "Val22"}),
                       ])),
      tags._TagSetItem(tag="TAG-3",
                       optional_features={
                           "Cat1": {"Val12"},
                           "Cat3": {"Val31"},
                       }),
  )
  tags.VALID_TAGS.update({t.tag for t in tag_set})
  tags.REQUIRED_FEATURES.update({t.tag: t.required_features for t in tag_set})
  tags.OPTIONAL_FEATURES.update({t.tag: t.optional_features for t in tag_set})


class ValidateTest(parameterized.TestCase):

  @parameterized.named_parameters([
      {
          "testcase_name": "NoFeaturesExpectedNonCompound",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "~",
              "features": "~",
              "is_compound": "FaLsE",
          },
      },
      {
          "testcase_name": "NoFeaturesExpectedNonCompoundWithMorphophonemics",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "FaLsE",
          },
      },
      {
          "testcase_name": "NoFeaturesExpectedCompoundWithMorphophonemics",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "RequiredFeaturesExpectedNonCompoundWithFeatures",
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "~",
              "features": "+[Cat1=Val12]+[Cat2=Val21]",
              "is_compound": "FaLsE",
          },
      },
      {
          "testcase_name": ("RequiredFeaturesExpectedNonCompoundWithFeaturesAnd"
                            "Morphophonemics"),
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]+[Cat2=Val21]",
              "is_compound": "FaLsE",
          },
      },
      {
          "testcase_name":
              "RequiredFeaturesExpectedCompoundWithFeaturesAndMorphophonemics",
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]+[Cat2=Val21]",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "OptionalFeaturesExpectedNonCompound",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "~",
              "features": "~",
              "is_compound": "FaLsE",
          },
      },
      {
          "testcase_name":
              "OptionalFeaturesExpectedNonCompoundWithMorphophonemics",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "FaLsE",
          },
      },
      {
          "testcase_name": "OptionalFeaturesExpectedNonCompoundWithFeatures",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "~",
              "features": "+[Cat1=Val12]",
              "is_compound": "FaLsE",
          },
      },
      {
          "testcase_name": ("OptionalFeaturesExpectedNonCompoundWithFeaturesAnd"
                            "Morphophonemics"),
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]",
              "is_compound": "FaLsE",
          },
      },
      {
          "testcase_name":
              "OptionalFeaturesExpectedCompoundWithMorphophonemics",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name":
              "OptionalFeaturesExpectedCompoundWithFeaturesAndMorphophonemics",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]",
              "is_compound": "TrUe",
          },
      },
  ])
  def test_success(self, entry):
    self.assertIsNone(validator.validate(entry))

  @parameterized.named_parameters([
      {
          "testcase_name": "MissingTag",
          "error": "Entry is missing fields: 'tag'",
          "entry": {
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "MissingRoot",
          "error": "Entry is missing fields: 'root'",
          "entry": {
              "tag": "TaG-1",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "MissingMorphophonemics",
          "error": "Entry is missing fields: 'morphophonemics'",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "MissingFeatures",
          "error": "Entry is missing fields: 'features'",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "MissingIsCompound",
          "error": "Entry is missing fields: 'is_compound'",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
          },
      },
      {
          "testcase_name": "MissingMultipleRequiredField",
          "error": ("Entry is missing fields: 'is_compound,"
                    " morphophonemics, root"),
          "entry": {
              "tag": "TaG-1",
              "features": "~",
          },
      },
      {
          "testcase_name": "EmptyTag",
          "error": "Entry fields have empty values: 'tag'",
          "entry": {
              "tag": "",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "EmptyRoot",
          "error": "Entry fields have empty values: 'root'",
          "entry": {
              "tag": "TaG-1",
              "root": "",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "EmptyMorphophonemics",
          "error": "Entry fields have empty values: 'morphophonemics'",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "EmptyFeatures",
          "error": "Entry fields have empty values: 'features'",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "EmptyIsCompound",
          "error": "Entry fields have empty values: 'is_compound'",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "",
          },
      },
      {
          "testcase_name": "MultipleEmptyRequiredField",
          "error": ("Entry fields have empty values: 'is_compound,"
                    " morphophonemics, root'"),
          "entry": {
              "tag": "TaG-1",
              "root": "",
              "morphophonemics": "",
              "features": "~",
              "is_compound": "",
          },
      },
      {
          "testcase_name": "TagContainsInfixWhitespace",
          "error": "Entry field values contain whitespace: 'tag'",
          "entry": {
              "tag": "TaG 1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "MorphophonemicsContainsInfixWhitespace",
          "error": "Entry field values contain whitespace: 'morphophonemics'",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "FeaturesContainsInfixWhitespace",
          "error": "Entry field values contain whitespace: 'features'",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1 = Val12]",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "MultipleFieldsContainsInfixWhitespace",
          "error": "Entry field values contain whitespace: 'features, tag'",
          "entry": {
              "tag": "TaG 3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1 = Val12]",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "InvalidTag",
          "error": ("Entry 'tag' field has invalid value. It can only be one of"
                    " the valid tags that are defined in"
                    " 'morphotactics_compiler/tags.py'."),
          "entry": {
              "tag": "Invalid-Tag",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "InvalidIsCompound",
          "error": ("Entry 'is_compound' field has invalid value. It can only"
                    " have the values 'true' or 'false'."),
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "invalid-is-compound",
          },
      },
      {
          "testcase_name": "InvalidMorphophonemics",
          "error":
              ("Entry is marked as ending with compounding marker but it is"
               " missing morphophonemics annotation."),
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "~",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "InvalidFeaturesInvalidPrefixCharacters",
          "error": "Entry features annotation is invalid.",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "foo+[Cat1=Val12]+[Cat3=Val31]",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "InvalidFeaturesInvalidInfixCharacters",
          "error": "Entry features annotation is invalid.",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]foo+[Cat3=Val31]",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "InvalidFeaturesInvalidSuffixCharacters",
          "error": "Entry features annotation is invalid.",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]+[Cat3=Val31]foo",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "NoRequiredFeatures",
          "error": "Entry is missing required features.",
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "MissingRequiredFeatures",
          "error": "Entry has invalid required feature category.",
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "InvalidRequiredFeatureCategory",
          "error": "Entry has invalid required feature category.",
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]+[Cat3=Val21]",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "InvalidRequiredFeatureValue",
          "error": "Entry has invalid required feature value.",
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]+[Cat2=Val23]",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "InvalidOptionalFeatureCategory",
          "error": "Entry has invalid optional features.",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat2=Val12]",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "InvalidOptionalFeatureValue",
          "error": "Entry has invalid optional features.",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val11]",
              "is_compound": "TrUe",
          },
      },
      {
          "testcase_name": "RedundantFeatures",
          "error": "Entry has features while it is not expected to have any.",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]",
              "is_compound": "TrUe",
          },
      },
  ])
  def test_raises_exception(self, error, entry):
    with self.assertRaisesRegexp(validator.InvalidLexiconEntryError, error):
      validator.validate(entry)


if __name__ == "__main__":
  absltest.main()
