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

"""Functions to morphologically analyze surface forms of Turkish words."""

import os
import pathlib
from typing import Generator, List, Optional

from external.openfst import pywrapfst

_Arc = pywrapfst.Arc
_Fst = pywrapfst.Fst
_SymbolTable = pywrapfst.SymbolTable
_Weight = pywrapfst.Weight


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


# Finite-state archive that contains the Turkish morphological analyzer FST
# is expected to be built into //src/analyzer/bin/turkish.far. See:
# //src/analyzer/build.
_ROOT_DIR = pathlib.Path(__file__).parent.parent
_FAR_PATH = os.path.join(_ROOT_DIR, "src", "analyzer", "bin", "turkish.far")
_FST_NAME = "turkish_morphological_analyzer"
_MODEL = _read_fst(_FAR_PATH, _FST_NAME)


def _input_fst(surface_form: str, symbol_table: _SymbolTable) -> _Fst:
  """Compiles given surface form in an FST.

  This function has an equivalent behaviour to the StringCompiler that
  is initialized with BYTE StringTokenType, see:

      @openfst//src/include/fst/string.h

  Args:
    surface_form: surface form to compile in an FST.
    symbol_table: symbol table which will be used to set as the symbol table
      of the compiled FST.

  Returns:
    FST that is compiled from the surface form.
  """
  fst = _Fst()
  last_state_index = fst.add_state()
  fst.set_start(last_state_index)

  for symbol_index in surface_form.encode("utf-8"):
    arc = _Arc(symbol_index, symbol_index, 0, last_state_index + 1)
    fst.add_arc(last_state_index, arc)
    last_state_index = fst.add_state()

  fst.set_final(last_state_index, 0)
  fst.set_input_symbols(symbol_table)
  fst.set_output_symbols(symbol_table)
  return fst


def _output_fst(model_fst: _Fst, input_fst: _Fst) -> _Fst:
  """Composes input FST with the model FST to create an FST with analyses."""
  input_fst.arcsort(sort_type="olabel")
  fst = pywrapfst.compose(input_fst, model_fst)
  return fst


def _extract_analyses(output_fst: _Fst,
                      state_index: int,
                      symbol_table: _SymbolTable,
                      symbols: Optional[List[str]] = []
                      ) -> Generator[str, None, None]:
  """Recursively extracts human-readable analyses from the output FST.

  This function extracts the human-readable analyses by walking over all
  possible paths from the start state of the output FST to its accept state.
  Joining the labels of the state transitions of these paths yield
  human-readable analyses.

  Args:
    output_fst: FST that is yielded after composing input and model FST.
    state_index: index of an FST state from which the paths to accept state will
      be traversed.
    symbol_table: symbol table of the Turkish morphological analyzer FST.
    symbols: tokens of human-readable analyses that are gathered from the start
      state of the output FST till the state that has the given state index.

  Yields:
    Human-readable analyses that are extracted from the output FST.
  """
  arcs = list(output_fst.arcs(state_index))

  if not arcs:  # is accept state, end of human-readable analyses.
    yield "".join(symbols)

  for arc in arcs:
    new_symbols = [s for s in symbols]
    symbol = symbol_table.find(arc.olabel)

    if symbol != "<eps>":
      new_symbols.append(symbol)

    yield from _extract_analyses(
        output_fst,
        arc.nextstate,
        symbol_table,
        new_symbols,
    )


def _remove_proper_feature(human_readable: str) -> str:
  """Removes proper feature from human-readable analysis."""
  human_readable = human_readable.replace("+[Proper=False]", "")
  human_readable = human_readable.replace("+[Proper=True]", "")
  return human_readable


def surface_form(surface_form: str,
                 use_proper_feature: Optional[bool] = True) -> List[str]:
  """Morphologically analyses given surface form.

  Args:
    surface_form: surface form of a Turkish word that is to be morphologically
      analyzed.
    use_proper_feature: if true includes 'Proper' feature in the morphological
      analyses.

  Returns:
    Human-readable morphological analyses that the Turkish morphological
    analyzer yields for the given surface form. Returns an empty list if the
    given surface form is not accepted as a Turkish word form.
  """
  input_ = _input_fst(surface_form, _MODEL.input_symbols())
  output = _output_fst(_MODEL, input_)

  if output.start() == -1:  # has no path to the accept state.
    return []

  human_readable = _extract_analyses(
      output,
      output.start(),
      _MODEL.input_symbols(),
  )

  if not use_proper_feature:
    human_readable = (_remove_proper_feature(hr) for hr in human_readable)

  return sorted(set(human_readable))
