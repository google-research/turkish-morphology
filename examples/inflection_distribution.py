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

"""Extracts distribution of inflections from morphological analyses."""

import collections
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
  igs = itertools.chain.from_iterable(a.ig for a in analyses)
  inflections = itertools.chain.from_iterable(ig.inflection for ig in igs)
  features = list((i.feature.category, i.feature.value) for i in inflections)

  total_count = len(features)
  counter = collections.Counter(features)

  print("Distribution of inflectional features in morphological analyses of"
        " the sentence '{}'\n".format(sentence))

  for category_value, count in counter.items():
    frequency = round(count / total_count * 100, 2)
    print("{}-{}: {}%".format(*category_value, frequency))


if __name__ == "__main__":
  app.run(main)
