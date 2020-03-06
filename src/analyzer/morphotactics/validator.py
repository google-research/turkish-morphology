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

"""Functions to validate morphotactics rewrite rule definitions."""

import re
from typing import List

from src.analyzer.morphotactics import common

_RuleDefinition = List[str]

_RULE_INPUT_REGEX = re.compile(
    # Inflectional group boundaries.
    r"(?:\)?\(\[[A-Z]+?\]-([^\W\d_]|')+?\[[A-z]+?=[A-z]+?\]|"
    # Inflectional morphemes and features.
    r"\+([^\W\d_]|['\.])*?\[[A-z]+?=[A-z0-9]+?\]|"
    # Proper noun analysis.
    r"\)\+\[Proper=(?:True|False)\]|"
    # Numbers.
    r"\d+?(?:\[[A-Z]+?\])?)+|"
    # Parenthesis or decimal point separators.
    r"[\(\.,]")
_RULE_OUTPUT_REGEX = re.compile(
    # Meta-morphemes.
    r"'?\+[^\W\d_]+|"
    # Morphophonemics of numbers.
    r"\d+(?:\.?\*?([^\W\d_]|['~])+\*?)?|"
    # Comma, full-stop or apostrophe.
    r"[',\.]")


class InvalidMorphotacticsRuleError(Exception):
  """Raised when a morphotactics rewrite rule definition is illformed."""


def _rule_has_expected_number_of_tokens(rule_definition: _RuleDefinition
                                        ) -> None:
  """Checks if rule definition has 4 tokens (from, to, output, input)."""
  if len(rule_definition) != 4:
    raise InvalidMorphotacticsRuleError(
        f"Expecting 4 tokens got {len(rule_definition)}.")


def _rule_has_non_empty_tokens(rule_definition: _RuleDefinition) -> None:
  """Checks if rule definition has no empty tokens."""
  if any(not t for t in rule_definition):
    raise InvalidMorphotacticsRuleError(
        "Rule definition contains empty tokens.")


def _rule_input_is_valid(input_label: str) -> None:
  """Checks if the input label of the rule definition is valid.

  Input label is valid if its structure is one of the following:
    - Epsilon (e.g. '<eps>')
    - Inflectional group boundary analysis (e.g. ')([JJ]-cA[Derivation=Ly]')
    - Inflectional morpheme analysis (e.g. '+mA[Polarity=Neg]')
    - Proper noun analysis (')+[Proper=True]' or ')+[Proper=False]')
    - Number analysis (e.g. '10[NN]')
    - Parenthesis or decimal point separators (e.g. ',' or '.').

  Args:
    input_label: input label of a morphotactics rule definition.

  Raises:
    InvalidMorphotacticsRuleError: input label of the morphotactics rule
        definition does not have a valid structure.
  """
  if input_label.lower() == common.EPSILON:
    return

  if not _RULE_INPUT_REGEX.fullmatch(input_label):
    raise InvalidMorphotacticsRuleError("Invalid rule input label.")


def _rule_output_is_valid(output_label: str) -> None:
  """Checks if the output label of the rule definition is valid.

  Output label is valid if its structure is one of the following:
    - Epsilon (e.g. '<eps>')
    - Meta-morpheme (e.g. '+lAr')
    - Morphophonemics of a number (e.g. '4*ört~*')
    - Comma, full-stop or apostrophe.

  Args:
    output_label: output label of a morphotactics rule definition.

  Raises:
    InvalidMorphotacticsRuleError: output label of the morphotactics rule
        definition does not have a valid structure.
  """
  if output_label.lower() == common.EPSILON:
    return

  if not _RULE_OUTPUT_REGEX.fullmatch(output_label):
    raise InvalidMorphotacticsRuleError("Invalid rule output label.")


def validate(rule_definition: _RuleDefinition) -> None:
  """Raises an exception if tokenized morphotactics rewrite rule is illformed.

  Args:
    rule_definition: morphotactics rule definition whose validity will be
        checked.

  Raises:
    InvalidMorphotacticsRuleError: morphotactics rule definition does not have
        4 tokens, or at least one of its tokens is empty string, or its input
        or output label token has invalid structure.
  """
  _rule_has_expected_number_of_tokens(rule_definition)
  _rule_has_non_empty_tokens(rule_definition)
  _rule_input_is_valid(rule_definition[2])
  _rule_output_is_valid(rule_definition[3])
