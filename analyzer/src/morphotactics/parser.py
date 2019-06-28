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

"""Functions to parse a tokenized morphotactics rewrite rule definition."""

from analyzer.src.morphotactics import rule_pb2


def _normalize(lines):
  """Normalizes the tokens of each morphotactics rewrite rule definition.

  This function converts the 'from' and 'to' state values to uppercase, and
  all bracketed 'output' and 'input' labels to lowercase (e.g. the rewrite rule
  'state-1 StAtE-2 +MetaMorpheme[Cat=Val] <EPS>' is normalized to
  'STATE-1 STATE-2 +MetaMorpheme[Cat=Val] <eps>'). Normalization is done
  in-place for each whitespace tokenized source line.

  Args:
    lines: list of list of str, each item of the list is a list of whitespace
        tokenized tokens of a line which defines a valid morphotactics rewrite
        rule.
  """
  def _bracketed(token):
    return token.startswith("<") and token.endswith(">")

  def _get_normalized(tokens):
    tokens[0] = tokens[0].upper()
    tokens[1] = tokens[1].upper()
    tokens[2] = tokens[2].lower() if _bracketed(tokens[2]) else tokens[2]
    tokens[3] = tokens[3].lower() if _bracketed(tokens[3]) else tokens[3]
    return tokens

  lines[:] = list(map(_get_normalized, lines))


def _create_rewrite_rule(tokens):
  """Creates a rewrite rule object from the rewrite rule definition tokens.

  Args:
    tokens: list of str, each item is a whitespace tokenized token of a line
        which defines a valid morphotactics rewrite rule.

  Returns:
    rule_pb2.RewriteRule, rewrite rule object that defines a state transition
    arc of the compiled morphocatics FST.
  """
  rule = rule_pb2.RewriteRule()
  rule.from_state = tokens[0]
  rule.to_state = tokens[1]
  rule.input = tokens[2]
  rule.output = tokens[3]
  return rule


def parse(lines):
  """Generates rewrite rules from the content of morphotactics source file.

  Note that this function assumes all input lines are valid, meaning that
  they should be first validated with
  //analyzer/fst/src/morphotactics/validator.py.

  Args:
    lines: list of list of str, each item of the list is a list of whitespace
        tokenized tokens of a line which defines a valid morphotactics rewrite
        rule.

  Returns:
    rule_pb2.RewriteRuleSet, array of rewrite rule objects that defines a
    subset of the state transition arcs of the compiled morphocatics FST.
  """
  _normalize(lines)
  rule_set = rule_pb2.RewriteRuleSet()
  rule_set.rule.extend(_create_rewrite_rule(l) for l in lines)
  return rule_set
