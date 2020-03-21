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

"""Functions to read Turkish morphological analyzer FST."""

import os
import pathlib

from external.openfst import pywrapfst

_Fst = pywrapfst.Fst

# Finite-state archive that contains the Turkish morphological analyzer FST
# is expected to be built into //src/analyzer/bin/turkish.far. See:
#     //src/analyzer/build.
_ROOT_DIR = pathlib.Path(__file__).parent.parent
_FAR_PATH = os.path.join(_ROOT_DIR, "src", "analyzer", "bin", "turkish.far")
_FST_NAME = "turkish_morphological_analyzer"


def _read_fst(far_path: str, fst_name: str) -> _Fst:
  """Reads FAR file from path and extracts the FST that has the sought name.

  Args:
    far_path: path to the finite-state archive that contains the sought FST.
    fst_name: name of the FST that will extracted from the finite-state archive.

  Returns:
    FST that has the sought name, which is extracted from the finite-state
    archive that is read from the path.
  """
  reader = pywrapfst.FarReader.open(far_path)
  return reader[fst_name]


ANALYZER = _read_fst(_FAR_PATH, _FST_NAME)
