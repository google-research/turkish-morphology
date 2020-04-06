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

"""Generates a sentence from morphological analyses."""

from turkish_morphology import decompose
from turkish_morphology import generate

from absl import app


def main(unused_argv):
  human_readables = [
      "(Ayşe[NNP]+[PersonNumber=A3sg]+[Possessive=Pnon]+[Case=Nom])",
      "(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+YA[Case=Dat])",
      ("(gel[VB]+[Polarity=Pos])([VN]-DHk[Derivation=PastNom]"
       "+[PersonNumber=A3sg]+SH[Possessive=P3sg]+NDA[Case=Loc])"),
      "(Ali[NNP]+[PersonNumber=A3sg]+[Possessive=Pnon]+[Case=Nom])",
      ("(git[VB]+[Polarity=Pos]+mHş[TenseAspectMood=Nar]+YDH[Copula=PastCop]"
       "+[PersonNumber=V3sg])"),
  ]
  analyses = map(decompose.human_readable_analysis, human_readables)
  tokens = map(generate.surface_form, analyses)
  print(f"Generated sentence: '{' '.join(tokens)}'")


if __name__ == "__main__":
  app.run(main)
