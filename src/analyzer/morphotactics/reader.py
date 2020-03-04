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
"""Functions to read text morphotactic model files."""

import collections
import itertools
from typing import Dict, List, Tuple

_RuleDefinition = List[str]


def _whitespace_trimmed(line: str) -> str:
  """Strips any leading and trailing whitespace off from the line."""
  return line.lstrip().rstrip()


def _empty(line: str) -> bool:
  """Returns True if line is empty (or only contains whitespace)."""
  return not line or line.isspace()


def _comment(line: str) -> bool:
  """Returns True if line is a comment line (starts with '#')."""
  return line.startswith("#")


def _rule(line: str) -> bool:
  """Returns True if the line defines an FST rule."""
  return not (_empty(line) or _comment(line))


def read_rule_definitions(path: str) -> Dict[int, _RuleDefinition]:
  """Reads morphotactics FST rule definitions from the path.

  Args:
    path: path to a text file which contains the definition of rewrite rules of
        morphotactics FST.

  Raises:
    IOError: morphotactics FST rule definitions cannot be read from the 'path'.

  Returns:
    Morphotactics FST rule definitions as a dictionary. Keys are indices of the
    lines of the source file, values are the list of whitespace tokenized tokens
    of each line. Content for lines those that are empty, only include comments,
    or only composed of whitespace characters are pruned and rule definitions
    are sorted by increasing line index. Returns an empty dictionary, if
    the text file does not contain any rule definitions.
  """
  with open(path, "r", encoding="utf-8") as reader:
    lines = reader.readlines()

  def _index_and_entry(index: int, line: str) -> Tuple[int, _RuleDefinition]:
    return index + 1, _whitespace_trimmed(line).split()

  rules = ((i, l) for i, l in enumerate(lines) if _rule(l))
  return collections.OrderedDict(itertools.starmap(_index_and_entry, rules))
