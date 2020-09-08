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

"""Turkish morphological analyzer FST utility functions."""

import os
import pathlib
from typing import Generator, Iterable, List, Optional

from external.openfst import pywrapfst

_Arc = pywrapfst.Arc
_Fst = pywrapfst.Fst
_SymbolTable = pywrapfst.SymbolTable

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


def compile(symbol_indices: Iterable[int], symbol_table: _SymbolTable) -> _Fst:
  """Compiles given sequnce of symbols in an FST.

  This function has similar behaviour to the StringCompiler that is initialized
  with BYTE StringTokenType, see:

      @openfst//src/include/fst/string.h

  Args:
    symbol_indices: indices of the sequence of symbols from the symbol table.
    symbol_table: symbol table which will be used to set as the symbol table
      of the compiled FST.

  Returns:
    FST that is compiled from the symbol indices.
  """
  fst = _Fst()
  last_state_index = fst.add_state()
  fst.set_start(last_state_index)

  for symbol_index in symbol_indices:
    arc = _Arc(symbol_index, symbol_index, 0, last_state_index + 1)
    fst.add_arc(last_state_index, arc)
    last_state_index = fst.add_state()

  fst.set_final(last_state_index, 0)
  fst.set_input_symbols(symbol_table)
  fst.set_output_symbols(symbol_table)
  return fst


def compose(this_fst: _Fst, that_fst: _Fst) -> _Fst:
  """Sorts the arcs of this FST and composes it with that FST."""
  this_fst.arcsort(sort_type="olabel")
  return pywrapfst.compose(this_fst, that_fst)


def extract_parses(
    fst: _Fst,
    state_index: int,
    label_type: str,
    symbol_table: Optional[_SymbolTable] = None,
    symbol_indices: Optional[List[int]] = []) -> Generator[str, None, None]:
  """Recursively extracts parses from the FST.

  This function extracts the parses by walking over all possible paths from the
  start state of the FST to its accept state. Joining the labels of the state
  transitions of these paths yield a parse.

  Args:
    fst: FST from which parses will be extracted.
    state_index: index of an FST state from which the paths to accept state will
      be traversed.
    label_type: from which tape parse symbols will be extracted (one of 'ilabel'
      or 'olabel').
    symbol_table: symbol table of the FST (only needed to look up complex
      symbols when label type is specified as 'olabel').
    symbol_indices: indices of symbols of a parse that are gathered from the
      start state of the FST till the state that has the given state index.

  Raises:
    AttributeError: label type is invalid.

  Yields:
    Parses that are extracted from the FST.
  """
  if label_type not in ("ilabel", "olabel"):
    raise AttributeError(f"Invalid label type: {label_type}")

  arcs = list(fst.arcs(state_index))

  if not arcs:  # is accept state, end of a parse.
    if label_type == "ilabel":
      yield bytes(symbol_indices).decode("utf-8")
    else:
      yield "".join(map(symbol_table.find, symbol_indices))

  for arc in arcs:
    new_symbol_indices = [s for s in symbol_indices]
    symbol_index = getattr(arc, label_type)

    if symbol_index != 0:  # skip <eps>.
      new_symbol_indices.append(symbol_index)

    yield from extract_parses(
        fst,
        arc.nextstate,
        label_type,
        symbol_table,
        new_symbol_indices,
    )
