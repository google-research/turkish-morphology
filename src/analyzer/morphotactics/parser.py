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
"""Functions to parse rule definitions into rewrite rule objects."""

from typing import List

from src.analyzer.morphotactics import rule_pb2

_RewriteRule = rule_pb2.RewriteRule
_RewriteRuleSet = rule_pb2.RewriteRuleSet
_RuleDefinition = List[str]


def _normalize(rule_definitions: List[_RuleDefinition]) -> None:
  """Normalizes the tokens of morphotactics rewrite rule definition.

  This function converts the 'from_state' and 'to_state' values to uppercase,
  and all bracketed 'output' and 'input' labels to lowercase (e.g. the rewrite
  rule 'state-1 StAtE-2 +MetaMorpheme[Cat=Val] <EPS>' is normalized to
  'STATE-1 STATE-2 +MetaMorpheme[Cat=Val] <eps>'). Normalization is done
  in-place.

  Args:
    rule_definitions: morphotactics rule definitions whose tokens will be
        normalized.
  """

  def _bracketed(token: str) -> bool:
    return token.startswith("<") and token.endswith(">")

  def _get_normalized(rule_definition):
    from_state, to_state, input_, output = rule_definition
    rule_definition[0] = from_state.upper()
    rule_definition[1] = to_state.upper()
    rule_definition[2] = input_.lower() if _bracketed(input_) else input_
    rule_definition[3] = output.lower() if _bracketed(output) else output
    return rule_definition

  rule_definitions[:] = list(map(_get_normalized, rule_definitions))


def _create_rewrite_rule(rule_definition: _RuleDefinition) -> _RewriteRule:
  """Creates a rewrite rule from the morphotactics rule definition.

  Args:
    rule_definition: morphotactics rule definition which will be used to
        generate a rewrite rule.

  Returns:
    Rewrite rule object that defines a state transition arc of the
    morphotactics FST.
  """
  rule = _RewriteRule()
  rule.from_state = rule_definition[0]
  rule.to_state = rule_definition[1]
  rule.input = rule_definition[2]
  rule.output = rule_definition[3]
  return rule


def parse(rule_definitions: List[_RuleDefinition]) -> _RewriteRuleSet:
  """Generates a rewrite rule set from morphotactics rule definitions.

  Note that this function assumes all input rule definitions are valid, meaning
  that they should be first validated with
  //src/analyzer/morphotactics/validator.py.

  Args:
    rule_definitions: morphotactics rule definitions which will be used in
        generating rewrite rules.

  Returns:
    Array of rewrite rule objects that defines a subset of the state transition
    arcs of the morphotactics FST.
  """
  _normalize(rule_definitions)
  rule_set = _RewriteRuleSet()
  rule_set.rule.extend(_create_rewrite_rule(d) for d in rule_definitions)
  return rule_set
