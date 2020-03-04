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
"""Functions to parse lexicon entries into rewrite rule objects."""

import itertools
from typing import Dict, Generator, Iterable, List

from src.analyzer.lexicon import tags
from src.analyzer.morphotactics import common
from src.analyzer.morphotactics import rule_pb2

_LexiconEntry = Dict[str, str]
_RewriteRule = rule_pb2.RewriteRule
_RewriteRuleSet = rule_pb2.RewriteRuleSet


def _lower(string: str) -> str:
  """Properly lowercase transforms Turkish string ("İ" -> "i", "I" -> "ı")."""
  return string.replace("İ", "i").replace("I", "ı").lower()


def _upper(string: str) -> str:
  """Properly uppercase transforms Turkish string ("i" -> "İ")."""
  return string.replace("i", "İ").upper()


def _capitalize(string: str) -> str:
  """Properly capitalizes Turkish string (string initial "i" -> "İ")."""
  if string.startswith("i"):
    string.replace("i", "İ", 1)

  return string.replace("I", "ı").capitalize()


def _format_root(root: str, tag: str) -> str:
  """Case formats the root annotation given the tag for lexicon entry."""
  formatting = tags.FORMATTING[tag]

  if formatting == "lower":
    return _lower(root)
  elif formatting == "upper":
    return _upper(root)
  elif formatting == "capitals":
    return _capitalize(root)

  return root


def _normalize(entries: Iterable[_LexiconEntry]) -> List[_LexiconEntry]:
  """Normalizes annotated values of each field of the lexicon entry.

  This function;
      - converts the value of the 'tag' field into uppercase.
      - converts the value of the 'is_compound' field (e.g. str('true') or
        str('false')) into boolean.
      - formats the value of the 'root' field according to the case specifiers
        defined in the FORMATTING dictionary of
        //morphotactics_compiler/lexicon/tags.py.
      - removes the value of the 'morphophonemics' and 'features' fields if
        they are not annotated.
      - for each lexicon entry annotation that has characters with circumflex in
        the value of the 'root' field, adds a new lexicon entry annotation that
        has the orthographic counterparts of the characters with circumflex in
        the value of the 'root' and 'morphophonemics' fields.

  Args:
    entries: lexicon entries whose annotations will be normalized.

  Returns:
    Lexicon entries whose annotations are normalized.
  """
  circumflex = {
      "â": "a",
      "î": "i",
      "û": "u",
  }

  def _normalize_entry(entry: _LexiconEntry) -> _LexiconEntry:
    entry["tag"] = entry["tag"].upper()
    entry["is_compound"] = entry["is_compound"].lower() == "true"
    entry["root"] = _format_root(entry["root"], entry["tag"])

    for field in ("morphophonemics", "features"):
      entry[field] = "" if entry[field] == "~" else entry[field]

    return entry

  def _root_has_circumflex(entry: _LexiconEntry) -> bool:
    return any(c in entry["root"] for c in circumflex.keys())

  def _make_entry(entry: _LexiconEntry) -> _LexiconEntry:
    fields_to_check = ("root", "morphophonemics")
    field_and_chars = itertools.product(fields_to_check, circumflex.items())
    normalized = entry.copy()

    for field, (with_, without) in field_and_chars:
      normalized[field] = normalized[field].replace(with_, without)

    return normalized

  normalized = [_normalize_entry(e) for e in entries]
  new_entries = (_make_entry(e) for e in normalized if _root_has_circumflex(e))
  normalized.extend(new_entries)
  return normalized


def _cross_classify(entries: Iterable[_LexiconEntry]) -> List[_LexiconEntry]:
  """Cross-classifies lexicon entries across parts of speech.

  This function adds a new lexicon entry by just rewriting its tag for each
  part-of-speech that is defined in the CROSS_CLASSIFY_AS dictionary of
  //morphotactics_compiler/lexicon/tags.py.

  While making new cross-classified lexicon entries removes the required
  (or optional) features, if required (or optional) features defined for the
  target part-of-speech in REQUIRED_FEATURES and OPTIONAL_FEATURES dictionaries
  of //morphotactics_compiler/lexicon/tags.py does not match the ones that are
  defined for the source part-of-speech.

  Args:
    entries: lexicon entries which will be cross-classified across parts of
        speech.

  Returns:
    Lexicon entries that are yielded after part-of-speech cross-classification.
  """

  def _new_features(old_features: str, old_tag: str, new_tag: str) -> str:
    if new_tag == "NOMP-CASE-BARE":
      return "+[PersonNumber=A3sg]+[Possessive=Pnon]+[Case=Bare]"

    old_required = tags.REQUIRED_FEATURES[old_tag]
    new_required = tags.REQUIRED_FEATURES[new_tag]

    if (old_required and old_required == new_required):
      return old_features

    old_optional = tags.OPTIONAL_FEATURES[old_tag]
    new_optional = tags.OPTIONAL_FEATURES[new_tag]

    if (old_optional and old_optional == new_optional):
      return old_features

    return ""

  def _make_entry(entry: _LexiconEntry, old_tag: str,
                  new_tag: str) -> _LexiconEntry:
    new_entry = entry.copy()
    new_entry["tag"] = new_tag
    new_entry["root"] = _format_root(new_entry["root"], new_tag)
    new_entry["features"] = _new_features(entry["features"], old_tag, new_tag)
    return new_entry

  def _new_entries(entry: _LexiconEntry
                  ) -> Generator[_LexiconEntry, None, None]:
    old_tag = entry["tag"]
    new_tags = tags.CROSS_CLASSIFY_AS[old_tag]
    args = itertools.product([entry], [old_tag], new_tags)
    yield from (_make_entry(*a) for a in args)

  cross_classified = list(entries)
  new_entries = itertools.chain.from_iterable(map(_new_entries, entries))
  cross_classified.extend(new_entries)
  return cross_classified


def _rule_input(entry: _LexiconEntry) -> str:
  """Returns the input label of a rewrite rule.

  Args:
    entry: lexicon entry whose root form, tag and features annotations are
        used to create a rewrite rule input label.

  Returns:
    Input label of a state transition arc of the morphotactics FST. Returns an
    input label which has the form '(Root[Tag]+[Cat1=Val_x]...+[Catn=Val_y]'
    (e.g. '(dümdüz[JJ]+[Emphasis=True]').
  """
  root = entry["root"]
  tag = tags.OUTPUT_AS[entry["tag"]]
  features = entry["features"]
  return f"({root}[{tag}]{features}"


def _rule_output(entry: _LexiconEntry) -> str:
  """Returns the output label of a rewrite rule.

  Args:
    entry: lexicon entry whose morphophonemics or root form annotation is used
        to create a rewrite rule output label.

  Returns:
    Output label of a state transition arc of the morphotactics FST. If lexicon
    entry has morphophonemics annotation, returns it as the output label.
    Otherwise, returns lowercase normalized root form as the output label.
  """
  if entry["morphophonemics"]:
    return entry["morphophonemics"]

  return _lower(entry["root"])


def _create_rewrite_rule(entry: _LexiconEntry) -> _RewriteRule:
  """Creates a rewrite rule from the lexicon entry.

  Args:
    entry: lexicon entry which will be used to generate a rewrite rule.

  Returns:
    Rewrite rule object that defines a state transition arc of the
    morphotactics FST.
  """
  rule = _RewriteRule()
  rule.from_state = common.START_STATE
  rule.to_state = entry["tag"]
  rule.input = _rule_input(entry)
  rule.output = _rule_output(entry)
  return rule


def parse(entries: Iterable[_LexiconEntry]) -> _RewriteRuleSet:
  """Generates a rewrite rule set from lexicon entries.

  Note that this function assumes all input lexicon entries are valid, meaning
  that they should be first validated with //src/analyzer/lexicon/validator.py.

  Args:
    entries: lexicon entries which will be used to generate rewrite rules.

  Returns:
    Array of rewrite rule objects that defines a subset of the state transition
    arcs of the morphotactics FST.
  """
  normalized = _normalize(entries)
  cross_classified = _cross_classify(normalized)
  state_entries = (e for e in cross_classified if e["tag"] in tags.FST_STATES)
  rule_set = _RewriteRuleSet()
  rule_set.rule.extend(map(_create_rewrite_rule, state_entries))
  return rule_set
