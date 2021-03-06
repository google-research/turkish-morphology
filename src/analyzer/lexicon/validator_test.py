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
      tags.TagSetItem(tag="TAG-1"),
      tags.TagSetItem(
          tag="TAG-2",
          required_features=collections.OrderedDict([
              ("Cat1", {"Val11", "Val12"}),
              ("Cat2", {"Val21", "Val22"}),
          ]),
      ),
      tags.TagSetItem(
          tag="TAG-3",
          optional_features={
              "Cat1": {"Val12"},
              "Cat3": {"Val31"},
          },
      ),
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
          "entry": {
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": "Entry is missing fields: 'tag'",
      },
      {
          "testcase_name": "MissingRoot",
          "entry": {
              "tag": "TaG-1",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": "Entry is missing fields: 'root'",
      },
      {
          "testcase_name": "MissingMorphophonemics",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": "Entry is missing fields: 'morphophonemics'",
      },
      {
          "testcase_name": "MissingFeatures",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "is_compound": "TrUe",
          },
          "message": "Entry is missing fields: 'features'",
      },
      {
          "testcase_name": "MissingIsCompound",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
          },
          "message": "Entry is missing fields: 'is_compound'",
      },
      {
          "testcase_name":
              "MissingMultipleRequiredField",
          "entry": {
              "tag": "TaG-1",
              "features": "~",
          },
          "message": ("Entry is missing fields: 'is_compound,"
                      " morphophonemics, root"),
      },
      {
          "testcase_name": "EmptyTag",
          "entry": {
              "tag": "",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": "Entry fields have empty values: 'tag'",
      },
      {
          "testcase_name": "EmptyRoot",
          "entry": {
              "tag": "TaG-1",
              "root": "",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": "Entry fields have empty values: 'root'",
      },
      {
          "testcase_name": "EmptyMorphophonemics",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": "Entry fields have empty values: 'morphophonemics'",
      },
      {
          "testcase_name": "EmptyFeatures",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "",
              "is_compound": "TrUe",
          },
          "message": "Entry fields have empty values: 'features'",
      },
      {
          "testcase_name": "EmptyIsCompound",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "",
          },
          "message": "Entry fields have empty values: 'is_compound'",
      },
      {
          "testcase_name":
              "MultipleEmptyRequiredField",
          "entry": {
              "tag": "TaG-1",
              "root": "",
              "morphophonemics": "",
              "features": "~",
              "is_compound": "",
          },
          "message": ("Entry fields have empty values: 'is_compound,"
                      " morphophonemics, root'"),
      },
      {
          "testcase_name": "TagContainsInfixWhitespace",
          "entry": {
              "tag": "TaG 1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": "Entry field values contain whitespace: 'tag'",
      },
      {
          "testcase_name": "MorphophonemicsContainsInfixWhitespace",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": "Entry field values contain whitespace: 'morphophonemics'",
      },
      {
          "testcase_name": "FeaturesContainsInfixWhitespace",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1 = Val12]",
              "is_compound": "TrUe",
          },
          "message": "Entry field values contain whitespace: 'features'",
      },
      {
          "testcase_name": "MultipleFieldsContainsInfixWhitespace",
          "entry": {
              "tag": "TaG 3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1 = Val12]",
              "is_compound": "TrUe",
          },
          "message": "Entry field values contain whitespace: 'features, tag'",
      },
      {
          "testcase_name":
              "InvalidTag",
          "entry": {
              "tag": "Invalid-Tag",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": ("Entry 'tag' field has invalid value. It can only be one"
                      " of the valid tags that are defined in"
                      " 'morphotactics_compiler/tags.py'."),
      },
      {
          "testcase_name":
              "InvalidIsCompound",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "invalid-is-compound",
          },
          "message": ("Entry 'is_compound' field has invalid value. It can only"
                      " have the values 'true' or 'false'."),
      },
      {
          "testcase_name":
              "InvalidMorphophonemics",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "~",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": ("Entry is marked as ending with compounding marker but it"
                      " is missing morphophonemics annotation."),
      },
      {
          "testcase_name": "InvalidFeaturesInvalidPrefixCharacters",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "foo+[Cat1=Val12]+[Cat3=Val31]",
              "is_compound": "TrUe",
          },
          "message": "Entry features annotation is invalid.",
      },
      {
          "testcase_name": "InvalidFeaturesInvalidInfixCharacters",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]foo+[Cat3=Val31]",
              "is_compound": "TrUe",
          },
          "message": "Entry features annotation is invalid.",
      },
      {
          "testcase_name": "InvalidFeaturesInvalidSuffixCharacters",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]+[Cat3=Val31]foo",
              "is_compound": "TrUe",
          },
          "message": "Entry features annotation is invalid.",
      },
      {
          "testcase_name": "NoRequiredFeatures",
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "~",
              "is_compound": "TrUe",
          },
          "message": "Entry is missing required features.",
      },
      {
          "testcase_name": "MissingRequiredFeatures",
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]",
              "is_compound": "TrUe",
          },
          "message": "Entry has invalid required feature category.",
      },
      {
          "testcase_name": "InvalidRequiredFeatureCategory",
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]+[Cat3=Val21]",
              "is_compound": "TrUe",
          },
          "message": "Entry has invalid required feature category.",
      },
      {
          "testcase_name": "InvalidRequiredFeatureValue",
          "entry": {
              "tag": "TaG-2",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]+[Cat2=Val23]",
              "is_compound": "TrUe",
          },
          "message": "Entry has invalid required feature value.",
      },
      {
          "testcase_name": "InvalidOptionalFeatureCategory",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat2=Val12]",
              "is_compound": "TrUe",
          },
          "message": "Entry has invalid optional features.",
      },
      {
          "testcase_name": "InvalidOptionalFeatureValue",
          "entry": {
              "tag": "TaG-3",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val11]",
              "is_compound": "TrUe",
          },
          "message": "Entry has invalid optional features.",
      },
      {
          "testcase_name": "RedundantFeatures",
          "entry": {
              "tag": "TaG-1",
              "root": "valid-root",
              "morphophonemics": "valid-morphophonemics",
              "features": "+[Cat1=Val12]",
              "is_compound": "TrUe",
          },
          "message": "Entry has features while it is not expected to have any.",
      },
  ])
  def test_raises_exception(self, entry, message):
    with self.assertRaisesRegexp(validator.InvalidLexiconEntryError, message):
      validator.validate(entry)


if __name__ == "__main__":
  absltest.main()
