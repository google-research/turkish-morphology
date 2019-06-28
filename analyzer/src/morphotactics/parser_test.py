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

"""Tests for analyzer.src.morphotactics.parser."""

import unittest

from analyzer.src.morphotactics import parser
from analyzer.src.morphotactics import rule_pb2
from parameterized import param
from parameterized import parameterized
from google.protobuf import text_format


class ParseTest(unittest.TestCase):

  @parameterized.expand([
      param(
          "EmptyLines",
          lines=[],
          expected_pbtxt=""
      ),
      param(
          "SingleLine",
          lines=[["STATE-1", "STATE-2", "+Morpheme[Cat=Val]", "+Morpheme"]],
          expected_pbtxt="""
          rule {
            from_state: 'STATE-1'
            to_state: 'STATE-2'
            input: '+Morpheme[Cat=Val]'
            output: '+Morpheme'
          }
          """
      ),
      param(
          "MultipleLines",
          lines=[
              ["STATE-1", "STATE-2", "+Morpheme1[Cat1=Val1]", "+Morpheme1"],
              ["STATE-3", "STATE-4", "+Morpheme2[Cat2=Val2]", "+Morpheme2"],
          ],
          expected_pbtxt="""
          rule {
            from_state: 'STATE-1'
            to_state: 'STATE-2'
            input: '+Morpheme1[Cat1=Val1]'
            output: '+Morpheme1'
          }
          rule {
            from_state: 'STATE-3'
            to_state: 'STATE-4'
            input: '+Morpheme2[Cat2=Val2]'
            output: '+Morpheme2'
          }
          """
      ),
      param(
          "NormalizesFromStateName",
          lines=[["sTaTe-1", "STATE-2", "+Morpheme[Cat=Val]", "+Morpheme"]],
          expected_pbtxt="""
          rule {
            from_state: 'STATE-1'
            to_state: 'STATE-2'
            input: '+Morpheme[Cat=Val]'
            output: '+Morpheme'
          }
          """
      ),
      param(
          "NormalizesToStateName",
          lines=[["STATE-1", "StAtE-2", "+Morpheme[Cat=Val]", "+Morpheme"]],
          expected_pbtxt="""
          rule {
            from_state: 'STATE-1'
            to_state: 'STATE-2'
            input: '+Morpheme[Cat=Val]'
            output: '+Morpheme'
          }
          """
      ),
      param(
          "NormalizesBracketedOutputToken",
          lines=[["STATE-1", "StAtE-2", "<BrAcKeTeD>", "+Morpheme"]],
          expected_pbtxt="""
          rule {
            from_state: 'STATE-1'
            to_state: 'STATE-2'
            input: '<bracketed>'
            output: '+Morpheme'
          }
          """
      ),
      param(
          "NormalizesBracketedInputToken",
          lines=[["STATE-1", "StAtE-2", "+Morpheme[Cat=Val]", "<BrAcKeTeD>"]],
          expected_pbtxt="""
          rule {
            from_state: 'STATE-1'
            to_state: 'STATE-2'
            input: '+Morpheme[Cat=Val]'
            output: '<bracketed>'
          }
          """
      ),
  ])
  def test_success(self, _, lines, expected_pbtxt):
    actual = parser.parse(lines)
    expected = rule_pb2.RewriteRuleSet()
    text_format.Parse(expected_pbtxt, expected)
    self.assertEqual(expected, actual)


if __name__ == "__main__":
  unittest.main()
