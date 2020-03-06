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

"""Tests for src.analyzer.morphotactics.validator."""

from src.analyzer.morphotactics import validator

from absl.testing import absltest
from absl.testing import parameterized


class ValidateTest(parameterized.TestCase):

  @parameterized.named_parameters([
      {
          "testcase_name": "EpsilonRuleInputAndOutput",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "<eps>",
          ],
      },
      {
          "testcase_name":
              "EpsilonRuleOutputIgBoundryRuleInput",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              ")([JJ]-HmsH[Derivation=Sim]",
              "<eps>",
          ],
      },
      {
          "testcase_name":
              "EpsilonRuleOutputInflectionMorphemeRuleInput",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "+NDAn[Case=Abl]",
              "<eps>",
          ],
      },
      {
          "testcase_name":
              "EpsilonRuleOutputProperNounAnalysisRuleInput",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              ")+[Proper=False]",
              "<eps>",
          ],
      },
      {
          "testcase_name":
              "EpsilonRuleOutputNumberRuleInput",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "1[NN]+'[Apostrophe=True]+HncH[NumberInf=Ord]",
              "<eps>",
          ],
      },
      {
          "testcase_name": "EpsilonRuleOutputDecimalPointSeparatorRuleInput",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              ".",
              "<eps>",
          ],
      },
      {
          "testcase_name": "EpsilonRuleInputMetaMorphemeRuleOutput",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "+cAğHz",
          ],
      },
      {
          "testcase_name": "EpsilonRuleInputNumberMorphophonemicsRuleOutput",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "00.*ü*",
          ],
      },
  ])
  def test_success(self, rule_definition):
    self.assertIsNone(validator.validate(rule_definition))

  @parameterized.named_parameters([
      {
          "testcase_name": "ExtraTokens",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "<eps>",
              "EXTRA-TOKEN",
          ],
          "error": "Expecting 4 tokens got 5.",
      },
      {
          "testcase_name": "MissingTokens",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
          ],
          "error": "Expecting 4 tokens got 2.",
      },
      {
          "testcase_name": "EmptyFromStateToken",
          "rule_definition": [
              "",
              "TO-STATE",
              "<eps>",
              "<eps>",
          ],
          "error": "Rule definition contains empty tokens.",
      },
      {
          "testcase_name": "EmptyToStateToken",
          "rule_definition": [
              "FROM-STATE",
              "",
              "<eps>",
              "<eps>",
          ],
          "error": "Rule definition contains empty tokens.",
      },
      {
          "testcase_name": "EmptyRuleInputToken",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "",
              "<eps>",
          ],
          "error": "Rule definition contains empty tokens.",
      },
      {
          "testcase_name": "EmptyRuleOutputToken",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "",
          ],
          "error": "Rule definition contains empty tokens.",
      },
      {
          "testcase_name": "InvalidPrefixCharactersInInputToken",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "foo)([TAG]-ki[Cat=Val]]",
              "<eps>",
          ],
          "error": "Invalid rule input label.",
      },
      {
          "testcase_name": "InvalidInfixCharactersInInputToken",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              ")foo+[Proper=True]",
              "<eps>",
          ],
          "error": "Invalid rule input label.",
      },
      {
          "testcase_name": "InvalidSuffixCharactersInInputToken",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "5[TAG]foo",
              "<eps>",
          ],
          "error": "Invalid rule input label.",
      },
      {
          "testcase_name": "InvalidRuleInputToken",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "Invalid-Input",
              "<eps>",
          ],
          "error": "Invalid rule input label.",
      },
      {
          "testcase_name": "InvalidRuleOutputToken",
          "rule_definition": [
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "Invalid-Output",
          ],
          "error": "Invalid rule output label.",
      },
  ])
  def test_raises_exception(self, rule_definition, error):
    with self.assertRaisesRegexp(validator.InvalidMorphotacticsRuleError,
                                 error):
      validator.validate(rule_definition)


if __name__ == "__main__":
  absltest.main()
