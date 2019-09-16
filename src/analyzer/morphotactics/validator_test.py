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

import unittest

from src.analyzer.morphotactics import validator
from parameterized import param
from parameterized import parameterized


class ValidateTest(unittest.TestCase):

  @parameterized.expand([
      param(
          "EpsilonRuleInputAndOutput",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "<eps>"
          ]
      ),
      param(
          "EpsilonRuleOutputIgBoundryRuleInput",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              ")([JJ]-HmsH[Derivation=Sim]",
              "<eps>"
          ]
      ),
      param(
          "EpsilonRuleOutputInflectionMorphemeRuleInput",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "+NDAn[Case=Abl]",
              "<eps>"
          ]
      ),
      param(
          "EpsilonRuleOutputProperNounAnalysisRuleInput",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              ")+[Proper=False]",
              "<eps>"
          ]
      ),
      param(
          "EpsilonRuleOutputNumberRuleInput",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "1[NN]+'[Apostrophe=True]+HncH[NumberInf=Ord]",
              "<eps>"
          ]
      ),
      param(
          "EpsilonRuleOutputDecimalPointSeparatorRuleInput",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              ".",
              "<eps>"
          ]
      ),
      param(
          "EpsilonRuleInputMetaMorphemeRuleOutput",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "+cAğHz"
          ]
      ),
      param(
          "EpsilonRuleInputNumberMorphophonemicsRuleOutput",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "00.*ü*"
          ]
      ),
  ])
  def test_success(self, _, tokens):
    self.assertIsNone(validator.validate(tokens))

  @parameterized.expand([
      param(
          "ExtraTokens",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "<eps>",
              "EXTRA-TOKEN"
          ],
          error="Expecting 4 tokens got 5."
      ),
      param(
          "MissingTokens",
          tokens=[
              "FROM-STATE",
              "TO-STATE"
          ],
          error="Expecting 4 tokens got 2."
      ),
      param(
          "EmptyFromStateToken",
          tokens=[
              "",
              "TO-STATE",
              "<eps>",
              "<eps>"
          ],
          error="Line contains empty tokens."
      ),
      param(
          "EmptyToStateToken",
          tokens=[
              "FROM-STATE",
              "",
              "<eps>",
              "<eps>"
          ],
          error="Line contains empty tokens."
      ),
      param(
          "EmptyRuleInputToken",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "",
              "<eps>"
          ],
          error="Line contains empty tokens."
      ),
      param(
          "EmptyRuleOutputToken",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              ""
          ],
          error="Line contains empty tokens."
      ),
      param(
          "InvalidPrefixCharactersInInputToken",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "foo)([TAG]-ki[Cat=Val]]",
              "<eps>"
          ],
          error="Invalid rule input label."
      ),
      param(
          "InvalidInfixCharactersInInputToken",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              ")foo+[Proper=True]",
              "<eps>"
          ],
          error="Invalid rule input label."
      ),
      param(
          "InvalidSuffixCharactersInInputToken",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "5[TAG]foo",
              "<eps>"
          ],
          error="Invalid rule input label."
      ),
      param(
          "InvalidRuleInputToken",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "Invalid-Input",
              "<eps>"
          ],
          error="Invalid rule input label."
      ),
      param(
          "InvalidRuleOutputToken",
          tokens=[
              "FROM-STATE",
              "TO-STATE",
              "<eps>",
              "Invalid-Output"
          ],
          error="Invalid rule output label."
      ),
  ])
  def test_raises_exception(self, _, tokens, error):
    with self.assertRaisesRegexp(validator.InvalidMorphotacticsRuleError,
                                 error):
      validator.validate(tokens)


if __name__ == "__main__":
  unittest.main()
