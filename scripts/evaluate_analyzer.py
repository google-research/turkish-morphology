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

"""Tool to evaluate coverage and hypothesis space of the morphological analyzer.
"""

import argparse
import collections
import glob
import io
import itertools
import logging
import multiprocessing
import os
import re
import subprocess


_BASE_PATH = os.path.dirname(os.path.abspath(__file__))


_ARG_PARSER = argparse.ArgumentParser(description="""
    This tools collects aggregated statistics on coverage, and average number
    of analysis and inflectional groups generated for word forms that are
    observed in a data set. It consumes data sets that are in CoNLL format.

    In order to run this tool you need to place your copy of Turkish treebank
    under //scripts/treebank (make this directory if it does not
    exists). All treebank files that are under this directory that has ".conll"
    file extension should be in CoNLL 2007 format. They will be picked up by
    this tool and used in calculating the statistics.""")
_ARG_PARSER.add_argument(
    "--far_path",
    default=os.path.join(_BASE_PATH, "../src/analyzer/bin/turkish.far"),
    help="""path to the FST archive which contains Turkish morphological
    analyzer.""")
_ARG_PARSER.add_argument(
    "--treebank_dir",
    default="scripts/treebank",
    help="""path to the directory which contains treebank files.""")


class EvaluationError(Exception):
  """Raised when failure/success of the analyzer cannot be determined."""


_SUCCESS_OUTPUT_REGEX = re.compile(
    r"Morphological analyses for the word '.+':(.+)",
    re.DOTALL)
_FAILURE_OUTPUT_REGEX = re.compile(
    r".+is not accepted as a Turkish word.+",
    re.DOTALL)
_IG_BOUNDARY_REGEX = re.compile(
    r"\(\[.+?\]-.+?")


# Ad-hoc container to store aggregated statistics.
class Statistics():
  success_count = 0
  failure_count = 0
  analysis_count_with_proper = 0
  ig_count_with_proper = 0
  analysis_count_without_proper = 0
  ig_count_without_proper = 0
  unparsed = set()


def _lower(string):
  """Properly lower transforms Turkish string ("İ" -> "i", "I" -> "ı")."""
  return string.replace("İ", "i").replace("I", "ı").lower()


def _read_tokens(treebank_dir):
  """Reads tokens from CoNLL data and returns them in a list."""

  def _extract_tokens_from(line):
    """Extracts token from a CoNLL data file line."""
    if line.isspace():  # Empty lines are sentence seperators.
      return

    column = line.split()

    if not len(column) >= 2:
      raise EvaluationError(
          f"Illformed line in source CoNLL data, only {len(column)}"
          f" whitespace separated columns found but word form is expected"
          f" to be on the second column.")

    token = column[1]

    if token != "_":  # It's an inflectional group, not a word form.
      yield from token.split("_")

  def _read_from(path):
    """Reads tokens from CoNLL data file that lives in the path."""
    logging.info("Reading tokens from '%s'", path)

    with io.open(path, "r", encoding="utf-8") as reader:
      line_tokens = (_extract_tokens_from(l) for l in reader)
      yield from itertools.chain.from_iterable(line_tokens)

  paths = glob.iglob(f"{treebank_dir}/*.conll")
  file_tokens = [_read_from(p) for p in paths]
  tokens = list(itertools.chain.from_iterable(file_tokens))

  if not tokens:
    raise EvaluationError(
        f"No tokens found in treebank files that are under '{treebank_dir}'.")

  return tokens


def _gather_analyses(word_form, far_path):
  """Gathers generated morphological analysis strings for a word form."""

  def _remove_proper(analysis):
    """Removes proper feature from the analysis string."""
    return analysis.replace("+[Proper=False]", "").replace("+[Proper=True]", "")

  output = subprocess.check_output(
      ["./print_analyses", f"--far_path={far_path}", f"--word={word_form}"],
      cwd=_BASE_PATH)

  success = _SUCCESS_OUTPUT_REGEX.match(output.decode("utf-8"))

  if success:
    with_proper = set([a for a in success.group(1).split("\n") if a])
    without_proper = set([_remove_proper(a) for a in with_proper])
    return word_form, with_proper, without_proper

  failure = _FAILURE_OUTPUT_REGEX.match(output.decode("utf-8"))

  if failure:
    return word_form, set(), set()

  raise EvaluationError(
      f"Cannot determine whether analyzer can parse the word or not given"
      f" the output it generates for the word form"
      f" '{word_form}'. The output is:\n{output}")


def _evaluate(word_forms, far_path):
  """Collects statistics on coverage, and generated analysis and IG counts."""
  statistics = Statistics()
  pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)

  def _ig_count(analysis):
    """Finds the number of inflectional groups in the analysis string."""
    return len(_IG_BOUNDARY_REGEX.findall(analysis)) + 1

  def _aggregate_stats(result):
    """Aggregates statistics for a word form."""
    word_form, with_proper, without_proper = result

    if not (with_proper and without_proper):
      statistics.failure_count += 1
      statistics.unparsed.add(word_form)
      return

    statistics.success_count += 1

    if with_proper:
      statistics.analysis_count_with_proper += len(with_proper)
      ig_count = sum([_ig_count(a) for a in with_proper])
      statistics.ig_count_with_proper += ig_count

    if without_proper:
      statistics.analysis_count_without_proper += len(without_proper)
      ig_count = sum([_ig_count(a) for a in without_proper])
      statistics.ig_count_without_proper += ig_count

  for word_form in word_forms:
    process_args = (word_form, far_path)
    pool.apply_async(_gather_analyses, process_args, callback=_aggregate_stats)

  pool.close()
  pool.join()
  return statistics


def _prepare_summary(tokens, word_forms, statistics):
  """Generates a human-readable evaluation summary."""
  if not tokens:
    raise EvaluationError(
        "Cannot generate evaluation summary without tokens.")

  if not word_forms:
    raise EvaluationError(
        "Cannot generate evaluation summary without word forms.")

  token_count = len(tokens)
  form_count = len(word_forms)
  coverage = statistics.success_count / form_count * 100
  success = statistics.success_count
  failure = statistics.failure_count
  analysis_with_proper = statistics.analysis_count_with_proper
  analysis_without_proper = statistics.analysis_count_without_proper
  ig_with_proper = statistics.ig_count_with_proper
  ig_without_proper = statistics.ig_count_without_proper

  if success:
    avg_analysis_with_proper = analysis_with_proper / success
    avg_analysis_without_proper = analysis_without_proper / success
    avg_ig_with_proper = ig_with_proper / analysis_with_proper
    avg_ig_without_proper = ig_without_proper / analysis_without_proper
  else:
    avg_analysis_with_proper = 0
    avg_analysis_without_proper = 0
    avg_ig_with_proper = 0
    avg_ig_without_proper = 0

  if statistics.unparsed:
    failures = "\n      ".join(u for u in statistics.unparsed)
  else:
    failures = "N\A"

  return f"""
  +++++ OVERALL +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

      Total number of tokens: {token_count}
      Number of unique word forms (after case-folding): {form_count}
      Number of success (word forms that can be parsed): {success}
      Number of failure (word forms that cannot be parsed): {failure}
      Coverage (%): {coverage}

  +++++ STATS WITH PROPER FEATURE +++++++++++++++++++++++++++++++++++++++++++++

      Total number of analysis generated: {analysis_with_proper}
      Avg. number of analysis per word form: {avg_analysis_with_proper}
      Total number of IGs generated: {ig_with_proper}
      Avg. number of IGs per analysis: {avg_ig_with_proper}

  +++++ STATS WITHOUT PROPER FEATURE ++++++++++++++++++++++++++++++++++++++++++

      Total number of analysis generated: {analysis_without_proper}
      Avg. number of analysis per word form: {avg_analysis_without_proper}
      Total number of IGs generated: {ig_with_proper}
      Avg. number of IGs per analysis: {avg_ig_without_proper}

  +++++ FAILURES ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

      {failures}

  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  """


def main(args):
  tokens = _read_tokens(args.treebank_dir)
  word_forms = set([_lower(t) for t in tokens])
  statistics = _evaluate(word_forms, args.far_path)
  summary = _prepare_summary(tokens, word_forms, statistics)
  print(summary)


if __name__ == "__main__":
  logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s %(levelname)s: %(message)s",
      datefmt="%H:%M:%S")
  main(_ARG_PARSER.parse_args())
