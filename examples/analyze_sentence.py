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

"""Morphologically analyzes words of a sentence."""

from turkish_morphology import analyze

from absl import app


def main(unused_argv):
  sentence = "Ayşe eve geldiğinde Ali gitmişti"
  tokens = sentence.split()

  print("Morphological analyses for the sentence '{}'\n".format(sentence))

  for token, analyses in zip(tokens, map(analyze.surface_form, tokens)):
    print("{}:\n{}\n".format(token, "\n".join(analyses)))


if __name__ == "__main__":
  app.run(main)
