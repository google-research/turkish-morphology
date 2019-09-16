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

"""Functions to read text source morphotactic files."""

import collections
import io
import itertools


def _whitespace_trimmed(line):
  """Strips any leading and trailing whitespace off from the line."""
  return line.lstrip().rstrip()


def _empty(line):
  """Returns True if line is empty (or only contains whitespace)."""
  return not line or line.isspace()


def _comment(line):
  """Returns True if line is a comment line (starts with '#')."""
  return line.startswith("#")


def _rule(line):
  """Returns True if the line defines an FST rule."""
  return not (_empty(line) or _comment(line))


def read_morphotactics_source(path):
  """Reads the content of text morphotactics source file from the file path.

  Args:
    path: string, path to a text file which contains the rewrite rules of
        morphotactics transducer.

  Raises:
    IOError: source file cannot be read from the 'path'.

  Returns:
    OrderedDict(int->list of str). Keys are indices of the lines of the source
    file, values are the list of whitespace tokenized tokens of each line. This
    dictionary does not contain the content for the lines that are empty, that
    only include comments, or only composed of whitespace characters. Items are
    sorted by increasing line index.
  """
  with io.open(path, "r", encoding="utf-8") as reader:
    lines = reader.readlines()

  def _index_and_entry(index, line):
    return index + 1, _whitespace_trimmed(line).split()

  rules = ((i, l) for i, l in enumerate(lines) if _rule(l))
  return collections.OrderedDict(itertools.starmap(_index_and_entry, rules))
