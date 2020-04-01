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

from typing import List, Optional

from turkish_morphology import fst


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
  symbol_table = fst.ANALYZER.input_symbols()
  input_ = fst.compile(surface_form.encode("utf-8"), symbol_table)
  output = fst.compose(input_, fst.ANALYZER)

  if output.start() == -1:  # has no path to the accept state.
    return []

  human_readable = fst.extract_parses(
      output,
      output.start(),
      "olabel",
      symbol_table,
  )

  if not use_proper_feature:
    human_readable = (_remove_proper_feature(hr) for hr in human_readable)

  return sorted(set(human_readable))
