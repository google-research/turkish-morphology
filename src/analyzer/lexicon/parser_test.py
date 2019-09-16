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

"""Tests for src.analyzer.lexicon.parser."""

import collections
import unittest

from src.analyzer.lexicon import parser
from src.analyzer.lexicon import tags
from src.analyzer.morphotactics import rule_pb2
from parameterized import param
from parameterized import parameterized
from google.protobuf import text_format


def setUpModule():
  # Inject valid test tags and their expected required and optional features,
  # cross classification pairs and word formatting specifiers to respective
  # dictionaries that are used in parsing. This allows us to use lexicon
  # entries that are constructed with these tags in below test cases.
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
              "Cat3": {"Val31", "Val32"},
          }
      ),
      tags._TagSetItem(
          tag="TAG-4",
          formatting="lower"
      ),
      tags._TagSetItem(
          tag="TAG-5",
          formatting="upper"
      ),
      tags._TagSetItem(
          tag="TAG-6",
          formatting="capitals"
      ),

      tags._TagSetItem(
          tag="TAG-7",
          output_as="TAG-7-OUTPUT"
      ),
      tags._TagSetItem(
          tag="TAG-8",
          cross_classify_as=("TAG-1",),
          required_features=collections.OrderedDict([
              ("Cat1", {"Val11", "Val12"}),
              ("Cat2", {"Val21", "Val22"}),
          ])
      ),
      tags._TagSetItem(
          tag="TAG-9",
          cross_classify_as=("TAG-1",),
          optional_features={
              "Cat1": {"Val11"},
              "Cat2": {"Val22"},
          }
      ),
      tags._TagSetItem(
          tag="TAG-10",
          cross_classify_as=("TAG-2",),
          required_features=collections.OrderedDict([
              ("Cat1", {"Val11", "Val12"}),
              ("Cat2", {"Val21", "Val22"}),
          ])
      ),
      tags._TagSetItem(
          tag="TAG-11",
          cross_classify_as=("TAG-3",),
          optional_features={
              "Cat3": {"Val31", "Val32"},
          }
      ),
      tags._TagSetItem(
          tag="TAG-12",
          cross_classify_as=("NOMP-CASE-BARE",)
      ),
      tags._TagSetItem(
          tag="TAG-13",
          is_fst_state=False,
          cross_classify_as=("TAG-1",)
      ),
  )
  tags.VALID_TAGS.update({t.tag for t in tag_set})
  tags.OUTPUT_AS.update(
      {t.tag: t.output_as if t.output_as else t.tag for t in tag_set})
  tags.FORMATTING.update({t.tag: t.formatting for t in tag_set})
  tags.FST_STATES.update({t.tag for t in tag_set if t.is_fst_state})
  tags.CROSS_CLASSIFY_AS.update({t.tag: t.cross_classify_as for t in tag_set})
  tags.REQUIRED_FEATURES.update({t.tag: t.required_features for t in tag_set})
  tags.OPTIONAL_FEATURES.update({t.tag: t.optional_features for t in tag_set})


class ParseTest(unittest.TestCase):

  @parameterized.expand([
      param(
          "EmptyEntries",
          entries=[],
          expected_pbtxt=""
      ),
      param(
          "SingleEntry",
          entries=[
              {"tag": "TAG-1",
               "root": "valid-root",
               "morphophonemics": "~",
               "features": "~",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(valid-root[TAG-1]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "MultipleEntry",
          entries=[
              {"tag": "TAG-2",
               "root": "valid-root-1",
               "morphophonemics": "~",
               "features": "+[Cat1=Val12]+[Cat2=Val21]",
               "is_compound": "False"},
              {"tag": "TAG-3",
               "root": "valid-root-2",
               "morphophonemics": "valid-morphophonemics",
               "features": "+[Cat3=Val32]",
               "is_compound": "True"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-2'
            input: '(valid-root-1[TAG-2]+[Cat1=Val12]+[Cat2=Val21]'
            output: 'valid-root-1'
          }
          rule {
            from_state: 'START'
            to_state: 'TAG-3'
            input: '(valid-root-2[TAG-3]+[Cat3=Val32]'
            output: 'valid-morphophonemics'
          }
          """
      ),
      param(
          "NormalizesTag",
          entries=[
              {"tag": "tAg-1",
               "root": "valid-root",
               "morphophonemics": "~",
               "features": "~",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(valid-root[TAG-1]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "NormalizesIsCompoundTrueAndPicksMorphophonemicsAsRuleOutput",
          entries=[
              {"tag": "TAG-1",
               "root": "valid-root",
               "morphophonemics": "valid-morphophonemics",
               "features": "~",
               "is_compound": "TrUe"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(valid-root[TAG-1]'
            output: 'valid-morphophonemics'
          }
          """
      ),
      param(
          "NormalizesIsCompoundFalseAndPicksRootAsRuleOutput",
          entries=[
              {"tag": "TAG-1",
               "root": "valid-root",
               "morphophonemics": "~",
               "features": "~",
               "is_compound": "fAlSe"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(valid-root[TAG-1]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "NormalizesRootToLowercase",
          entries=[
              {"tag": "tAg-4",
               "root": "VaLID-RoOt",
               "morphophonemics": "~",
               "features": "~",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-4'
            input: '(valıd-root[TAG-4]'
            output: 'valıd-root'
          }
          """
      ),
      param(
          "NormalizesRootToUppercase",
          entries=[
              {"tag": "tAg-5",
               "root": "VaLiD-RoOt",
               "morphophonemics": "~",
               "features": "~",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-5'
            input: '(VALİD-ROOT[TAG-5]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "NormalizesRootToCapitalized",
          entries=[
              {"tag": "tAg-6",
               "root": "İ-VaLID-RoOt",
               "morphophonemics": "~",
               "features": "~",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-6'
            input: '(İ-valıd-root[TAG-6]'
            output: 'i-valıd-root'
          }
          """
      ),
      param(
          "NormalizesCharactersWithCircumflexWithEmptyMorphotactics",
          entries=[
              {"tag": "TAG-1",
               "root": "vâlîd-root",
               "morphophonemics": "~",
               "features": "~",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(vâlîd-root[TAG-1]'
            output: 'vâlîd-root'
          }
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(valid-root[TAG-1]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "NormalizesCharactersWithCircumflexWithNonEmptyMorphotactics",
          entries=[
              {"tag": "TAG-1",
               "root": "vâlîd-root",
               "morphophonemics": "vâlîd-morphophonemics",
               "features": "~",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(vâlîd-root[TAG-1]'
            output: 'vâlîd-morphophonemics'
          }
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(valid-root[TAG-1]'
            output: 'valid-morphophonemics'
          }
          """
      ),
      param(
          "RewritesOutputTag",
          entries=[
              {"tag": "TAG-7",
               "root": "valid-root",
               "morphophonemics": "~",
               "features": "~",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-7'
            input: '(valid-root[TAG-7-OUTPUT]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "CrossClassifiesAndRemovesRequiredFeatures",
          entries=[
              {"tag": "TAG-8",
               "root": "valid-root",
               "morphophonemics": "~",
               "features": "+[Cat1=Val12]+[Cat2=Val21]",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-8'
            input: '(valid-root[TAG-8]+[Cat1=Val12]+[Cat2=Val21]'
            output: 'valid-root'
          }
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(valid-root[TAG-1]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "CrossClassifiesAndRemovesOptionalFeatures",
          entries=[
              {"tag": "TAG-9",
               "root": "valid-root",
               "morphophonemics": "~",
               "features": "+[Cat2=Val22]",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-9'
            input: '(valid-root[TAG-9]+[Cat2=Val22]'
            output: 'valid-root'
          }
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(valid-root[TAG-1]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "CrossClassifiesWithMatchingRequiredFeatures",
          entries=[
              {"tag": "TAG-10",
               "root": "valid-root",
               "morphophonemics": "~",
               "features": "+[Cat1=Val12]+[Cat2=Val21]",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-10'
            input: '(valid-root[TAG-10]+[Cat1=Val12]+[Cat2=Val21]'
            output: 'valid-root'
          }
          rule {
            from_state: 'START'
            to_state: 'TAG-2'
            input: '(valid-root[TAG-2]+[Cat1=Val12]+[Cat2=Val21]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "CrossClassifiesWithMatchingOptionalFeatures",
          entries=[
              {"tag": "TAG-11",
               "root": "valid-root",
               "morphophonemics": "~",
               "features": "+[Cat3=Val31]",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-11'
            input: '(valid-root[TAG-11]+[Cat3=Val31]'
            output: 'valid-root'
          }
          rule {
            from_state: 'START'
            to_state: 'TAG-3'
            input: '(valid-root[TAG-3]+[Cat3=Val31]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "CrossClassifiesAndAddsBareCaseMarkedNominalPredicateFeatures",
          entries=[
              {"tag": "TAG-12",
               "root": "valid-root",
               "morphophonemics": "~",
               "features": "~",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-12'
            input: '(valid-root[TAG-12]'
            output: 'valid-root'
          }
          rule {
            from_state: 'START'
            to_state: 'NOMP-CASE-BARE'
            input: '(valid-root[NOMP]+[PersonNumber=A3sg]+[Possessive=Pnon]+[Case=Bare]'
            output: 'valid-root'
          }
          """
      ),
      param(
          "DoesNotCreateRewriteRuleForEntryWithNonFstStateTag",
          entries=[
              {"tag": "TAG-13",
               "root": "valid-root",
               "morphophonemics": "~",
               "features": "~",
               "is_compound": "False"},
          ],
          expected_pbtxt="""
          rule {
            from_state: 'START'
            to_state: 'TAG-1'
            input: '(valid-root[TAG-1]'
            output: 'valid-root'
          }
          """
      ),
  ])
  def test_success(self, _, entries, expected_pbtxt):
    actual = parser.parse(entries)
    expected = rule_pb2.RewriteRuleSet()
    text_format.Parse(expected_pbtxt, expected)
    self.assertEqual(expected, actual)


if __name__ == "__main__":
  unittest.main()
