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
"""Functions to read TSV structured lexicon files."""

import collections
import io
import itertools
from typing import Dict, List, Tuple

_LexiconEntry = Dict[str, str]


def _whitespace_trimmed(line: str) -> str:
  """Strips any leading and trailing whitespace off from the line."""
  return line.lstrip().rstrip()


def _empty(line: str) -> bool:
  """Returns True if line is empty (or only contains whitespace)."""
  return not line or line.isspace()


def _split(line: str) -> List[str]:
  """Returns a list of whitespace trimmed columns that compose the line."""
  return [_whitespace_trimmed(c) for c in line.split("\t")]


def read_lexicon_entries(path: str) -> Dict[int, _LexiconEntry]:
  """Reads lexicon entries of the TSV structured lexicon file from the path.

  Args:
    path: path to a file which contains TSV dump of lexicon entries.

  Raises:
    IOError: lexicon entries cannot be read from the 'path'.

  Returns:
    Lexicon file content as a dictionary. Keys are indices of the rows of the
    source TSV, values are the lexicon entries as dictionaries that contain
    field-value pairs for the columns of each row. Content for empty rows are
    pruned and lexicon entries are sorted by increasing row index. Returns an
    empty dictionary, if the TSV dump does not contain any lexicon entries.
  """
  with io.open(path, "r", encoding="utf-8") as reader:
    lines = reader.readlines()

  # Line 1 is assumed to be the TSV header. Any line below the header is
  # assumed to be a lexicon entry.
  header, entries = lines[0], lines[1:]

  if not entries:
    return collections.OrderedDict()

  field_names = _split(header)

  def _index_and_entry(index: int, line: str) -> Tuple[int, _LexiconEntry]:
    return index + 2, dict(zip(field_names, _split(line)))

  non_empty = ((i, l) for i, l in enumerate(entries) if not _empty(l))
  return collections.OrderedDict(itertools.starmap(_index_and_entry, non_empty))
