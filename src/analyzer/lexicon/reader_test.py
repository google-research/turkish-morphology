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
"""Tests for src.analyzer.lexicon.reader."""

import collections
import os

from src.analyzer.lexicon import reader

from absl.testing import absltest
from absl.testing import parameterized

_TESTDATA_DIR = "src/analyzer/lexicon/testdata"


def _read_file(path):
  with open(path, "r") as f:
    read = f.read()
  return read


class ReadLexiconEntriesTest(parameterized.TestCase):

  @parameterized.named_parameters([
      {
          "testcase_name":
              "ValidLexiconWithHeaderAndEntries",
          "basename":
              "valid_entries_1",
          "expected":
              collections.OrderedDict((
                  (2, {
                      "tag": "Nn",
                      "root": "ABANOZ",
                      "morphophonemics": "~",
                      "features": "~",
                      "is_compound": "FALSE",
                  }),
                  (3, {
                      "tag": "nN",
                      "root": "âhît",
                      "morphophonemics": "âhî?t~",
                      "features": "~",
                      "is_compound": "FaLsE",
                  }),
                  (4, {
                      "tag": "nn",
                      "root": "ördekbaşı",
                      "morphophonemics": "ördekbaş",
                      "features": "~",
                      "is_compound": "true",
                  }),
                  (6, {
                      "tag": "Jj",
                      "root": "KIZIL",
                      "morphophonemics": "~",
                      "features": "~",
                      "is_compound": "FALSE",
                  }),
                  (7, {
                      "tag": "jJ",
                      "root": "kopkoyu",
                      "morphophonemics": "~",
                      "features": "+[Emphasis=True]",
                      "is_compound": "false",
                  }),
                  (8, {
                      "tag": "in",
                      "root": "ArT",
                      "morphophonemics": "~",
                      "features": "+[ComplementType=CGen]",
                      "is_compound": "FALSE",
                  }),
              )),
      },
      {
          "testcase_name": "InvalidLexiconWithOnlyHeader",
          "basename": "invalid_only_header",
          "expected": collections.OrderedDict(),
      },
  ])
  def test_success(self, basename, expected):
    path = os.path.join(_TESTDATA_DIR, f"{basename}.tsv")
    actual = reader.read_lexicon_entries(path)
    self.assertDictEqual(expected, actual)

  @parameterized.named_parameters([
      {
          "testcase_name": "InvalidPath",
          "path": os.path.join(_TESTDATA_DIR, "invalid_path.tsv"),
          "exception": IOError,
      },
      {
          "testcase_name": "EmptyPath",
          "path": "",
          "exception": IOError,
      },
  ])
  def test_raises_exception(self, path, exception):
    with self.assertRaises(exception):
      reader.read_lexicon_entries(path)


if __name__ == "__main__":
  absltest.main()
