# coding=utf-8
# Copyright 2020 The Google Research Authors.
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

"""Tests for turkish_morphology.generate."""

import os

from turkish_morphology import analysis_pb2
from turkish_morphology import generate

from absl.testing import absltest
from absl.testing import parameterized
from google.protobuf import text_format

_TESTDATA_DIR = "turkish_morphology/testdata"


def _read_file(path):
  with open(path, "r") as f:
    read = f.read()
  return read


def _read_analysis(basename):
  path = os.path.join(_TESTDATA_DIR, f"{basename}.pbtxt")
  return text_format.Parse(_read_file(path), analysis_pb2.Analysis())


class SurfaceFormTest(parameterized.TestCase):

  @parameterized.named_parameters([
      {
          "testcase_name": "SingleInflectionalGroupsWithProperFeature",
          "basename": "araba_with_proper",
          "expected": "arabalarda",
      },
      {
          "testcase_name": "SingleInflectionalGroupsWithoutProperFeature",
          "basename": "araba_without_proper",
          "expected": "arabalarda",
      },
      {
          "testcase_name": "MultipleInflectionalGroupsWithProperFeature",
          "basename": "yasa_with_proper",
          "expected": "yaşadıklarımdan",
      },
      {
          "testcase_name": "MultipleInflectionalGroupsWithoutProperFeature",
          "basename": "yasa_without_proper",
          "expected": "yaşadıklarımdan",
      },
  ])
  def test_success(self, basename, expected):
    analysis = _read_analysis(basename)
    actual = generate.surface_form(analysis)
    self.assertEqual(expected, actual)

  def test_failure(self):
    analysis = _read_analysis("invalid_oov_root")
    actual = generate.surface_form(analysis)
    self.assertEqual("", actual)


if __name__ == "__main__":
  absltest.main()
