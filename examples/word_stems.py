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

"""Extracts word stems from morphological analyses."""

import itertools
from typing import Generator

from turkish_morphology import analysis_pb2
from turkish_morphology import analyze
from turkish_morphology import decompose

from absl import app


def _analyze(token: str) -> Generator[analysis_pb2.Analysis, None, None]:
  human_readables = analyze.surface_form(token, use_proper_feature=False)
  yield from map(decompose.human_readable_analysis, human_readables)


def main(unused_argv):
  sentence = "Ayşe eve geldiğinde Ali gitmişti"
  tokens = sentence.split()

  analyses = itertools.chain.from_iterable(_analyze(t) for t in tokens)
  word_stems = set(a.ig[0].root.morpheme.lower() for a in analyses)

  print("Unique word stems that appear in morphological analyses of the"
        " sentence '{}'\n".format(sentence))

  for word_stem in sorted(word_stems):
    print(word_stem)


if __name__ == "__main__":
  app.run(main)
