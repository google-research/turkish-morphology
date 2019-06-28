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

"""Tests for analyzer.src.lexicon.validator."""

import collections
import unittest

from analyzer.src.lexicon import tags
from analyzer.src.lexicon import validator
from parameterized import param
from parameterized import parameterized


def setUpModule():
  # Inject valid test tags and their expected required and optional features to
  # respective dictionaries that are used in validation. This allows us to use
  # lexicon entries that are constructed with these tags and features in below
  # test cases.
  tag_set = (
      tags._TagSetItem(
          tag="TAG-1",
      ),
      tags._TagSetItem(
          tag="TAG-2",
          required_features=collections.OrderedDict([
              ("Cat1", {"Val11", "Val12"}),
              ("Cat2", {"Val21", "Val22"}),
          ])
      ),
      tags._TagSetItem(
          tag="TAG-3",
          optional_features={
              "Cat1": {"Val12"},
              "Cat3": {"Val31"},
          }
      ),
  )
  tags.VALID_TAGS.update({t.tag for t in tag_set})
  tags.REQUIRED_FEATURES.update({t.tag: t.required_features for t in tag_set})
  tags.OPTIONAL_FEATURES.update({t.tag: t.optional_features for t in tag_set})


class ValidateTest(unittest.TestCase):

  @parameterized.expand([
      param(
          "NoFeaturesExpectedNonCompound",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "~",
                 "features": "~",
                 "is_compound": "FaLsE"}
      ),
      param(
          "NoFeaturesExpectedNonCompoundWithMorphophonemics",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "FaLsE"}
      ),
      param(
          "NoFeaturesExpectedCompoundWithMorphophonemics",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "RequiredFeaturesExpectedNonCompoundWithFeatures",
          entry={"tag": "TaG-2",
                 "root": "valid-root",
                 "morphophonemics": "~",
                 "features": "+[Cat1=Val12]+[Cat2=Val21]",
                 "is_compound": "FaLsE"}
      ),
      param(
          "RequiredFeaturesExpectedNonCompoundWithFeaturesAndMorphophonemics",
          entry={"tag": "TaG-2",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val12]+[Cat2=Val21]",
                 "is_compound": "FaLsE"}
      ),
      param(
          "RequiredFeaturesExpectedCompoundWithFeaturesAndMorphophonemics",
          entry={"tag": "TaG-2",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val12]+[Cat2=Val21]",
                 "is_compound": "TrUe"}
      ),
      param(
          "OptionalFeaturesExpectedNonCompound",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "~",
                 "features": "~",
                 "is_compound": "FaLsE"}
      ),
      param(
          "OptionalFeaturesExpectedNonCompoundWithMorphophonemics",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "FaLsE"}
      ),
      param(
          "OptionalFeaturesExpectedNonCompoundWithFeatures",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "~",
                 "features": "+[Cat1=Val12]",
                 "is_compound": "FaLsE"}
      ),
      param(
          "OptionalFeaturesExpectedNonCompoundWithFeaturesAndMorphophonemics",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val12]",
                 "is_compound": "FaLsE"}
      ),
      param(
          "OptionalFeaturesExpectedCompoundWithMorphophonemics",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "OptionalFeaturesExpectedCompoundWithFeaturesAndMorphophonemics",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val12]",
                 "is_compound": "TrUe"}
      ),
  ])
  def test_success(self, _, entry):
    self.assertIsNone(validator.validate(entry))

  @parameterized.expand([
      param(
          "MissingTag",
          error="Entry is missing fields: 'tag'",
          entry={"root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "MissingRoot",
          error="Entry is missing fields: 'root'",
          entry={"tag": "TaG-1",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "MissingMorphophonemics",
          error="Entry is missing fields: 'morphophonemics'",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "MissingFeatures",
          error="Entry is missing fields: 'features'",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "is_compound": "TrUe"}
      ),
      param(
          "MissingIsCompound",
          error="Entry is missing fields: 'is_compound'",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~"}
      ),
      param(
          "MissingMultipleRequiredField",
          error=("Entry is missing fields: 'is_compound,"
                 " morphophonemics, root"),
          entry={"tag": "TaG-1",
                 "features": "~"}
      ),
      param(
          "EmptyTag",
          error="Entry fields have empty values: 'tag'",
          entry={"tag": "",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "EmptyRoot",
          error="Entry fields have empty values: 'root'",
          entry={"tag": "TaG-1",
                 "root": "",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "EmptyMorphophonemics",
          error="Entry fields have empty values: 'morphophonemics'",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "EmptyFeatures",
          error="Entry fields have empty values: 'features'",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "",
                 "is_compound": "TrUe"}
      ),
      param(
          "EmptyIsCompound",
          error="Entry fields have empty values: 'is_compound'",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": ""}
      ),
      param(
          "MultipleEmptyRequiredField",
          error=("Entry fields have empty values: 'is_compound,"
                 " morphophonemics, root'"),
          entry={"tag": "TaG-1",
                 "root": "",
                 "morphophonemics": "",
                 "features": "~",
                 "is_compound": ""}
      ),
      param(
          "TagContainsInfixWhitespace",
          error="Entry field values contain whitespace: 'tag'",
          entry={"tag": "TaG 1",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "MorphophonemicsContainsInfixWhitespace",
          error="Entry field values contain whitespace: 'morphophonemics'",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "valid morphophonemics",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "FeaturesContainsInfixWhitespace",
          error="Entry field values contain whitespace: 'features'",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1 = Val12]",
                 "is_compound": "TrUe"}
      ),
      param(
          "MultipleFieldsContainsInfixWhitespace",
          error="Entry field values contain whitespace: 'features, tag'",
          entry={"tag": "TaG 3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1 = Val12]",
                 "is_compound": "TrUe"}
      ),
      param(
          "InvalidTag",
          error=("Entry 'tag' field has invalid value. It can only be one of"
                 " the valid tags that are defined in"
                 " 'morphotactics_compiler/tags.py'."),
          entry={"tag": "Invalid-Tag",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "InvalidIsCompound",
          error=("Entry 'is_compound' field has invalid value. It can only"
                 " have the values 'true' or 'false'."),
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "invalid-is-compound"}
      ),
      param(
          "InvalidMorphophonemics",
          error=("Entry is marked as ending with compounding marker but it is"
                 " missing morphophonemics annotation."),
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "~",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "InvalidFeaturesInvalidPrefixCharacters",
          error="Entry features annotation is invalid.",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "foo+[Cat1=Val12]+[Cat3=Val31]",
                 "is_compound": "TrUe"}
      ),
      param(
          "InvalidFeaturesInvalidInfixCharacters",
          error="Entry features annotation is invalid.",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val12]foo+[Cat3=Val31]",
                 "is_compound": "TrUe"}
      ),
      param(
          "InvalidFeaturesInvalidSuffixCharacters",
          error="Entry features annotation is invalid.",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val12]+[Cat3=Val31]foo",
                 "is_compound": "TrUe"}
      ),
      param(
          "NoRequiredFeatures",
          error="Entry is missing required features.",
          entry={"tag": "TaG-2",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "~",
                 "is_compound": "TrUe"}
      ),
      param(
          "MissingRequiredFeatures",
          error="Entry has invalid required feature category.",
          entry={"tag": "TaG-2",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val12]",
                 "is_compound": "TrUe"}
      ),
      param(
          "InvalidRequiredFeatureCategory",
          error="Entry has invalid required feature category.",
          entry={"tag": "TaG-2",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val12]+[Cat3=Val21]",
                 "is_compound": "TrUe"}
      ),
      param(
          "InvalidRequiredFeatureValue",
          error="Entry has invalid required feature value.",
          entry={"tag": "TaG-2",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val12]+[Cat2=Val23]",
                 "is_compound": "TrUe"}
      ),
      param(
          "InvalidOptionalFeatureCategory",
          error="Entry has invalid optional features.",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat2=Val12]",
                 "is_compound": "TrUe"}
      ),
      param(
          "InvalidOptionalFeatureValue",
          error="Entry has invalid optional features.",
          entry={"tag": "TaG-3",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val11]",
                 "is_compound": "TrUe"}
      ),
      param(
          "RedundantFeatures",
          error="Entry has features while it is not expected to have any.",
          entry={"tag": "TaG-1",
                 "root": "valid-root",
                 "morphophonemics": "valid-morphophonemics",
                 "features": "+[Cat1=Val12]",
                 "is_compound": "TrUe"}
      ),
  ])
  def test_raises_exception(self, _, error, entry):
    with self.assertRaisesRegexp(validator.InvalidLexiconEntryError, error):
      validator.validate(entry)


if __name__ == "__main__":
  unittest.main()
