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

"""Prints all possible morphological analysis strings for a given Turkish word.
"""

from turkish_morphology import analyze

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string("word", None, "Word to morphologically analyze.")

flags.mark_flag_as_required("word")


def main(unused_argv):
  analyses = analyze.surface_form(FLAGS.word)

  if analyses:
    print(f"Morphological analyses for the word '{FLAGS.word}':")
    for analysis in analyses:
      print(analysis)
  else:
    print(f"'{FLAGS.word}' is not accepted as a Turkish word")


if __name__ == "__main__":
  app.run(main)
