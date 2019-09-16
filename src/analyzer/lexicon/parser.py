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

"""Functions to parse lexicon entry annotations into rewrite rule objects."""

import itertools

from src.analyzer.lexicon import tags
from src.analyzer.morphotactics import common
from src.analyzer.morphotactics import rule_pb2


def _lower(string):
  """Properly lowercase transforms Turkish string ("İ" -> "i", "I" -> "ı")."""
  return string.replace("İ", "i").replace("I", "ı").lower()


def _upper(string):
  """Properly uppercase transforms Turkish string ("i" -> "İ")."""
  return string.replace("i", "İ").upper()


def _capitalize(string):
  """Properly capitalizes Turkish string (string initial "i" -> "İ")."""
  if string.startswith("i"):
    string.replace("i", "İ", 1)

  return string.replace("I", "ı").capitalize()


def _format_root(root, tag):
  """Case formats the root annotation given the tag for lexicon entry."""
  formatting = tags.FORMATTING[tag]

  if formatting == "lower":
    return _lower(root)
  elif formatting == "upper":
    return _upper(root)
  elif formatting == "capitals":
    return _capitalize(root)

  return root


def _normalize(entries):
  """Normalizes annotated values of each field of lexicon entry annotations.

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
    entries: list of dict(str->str), each item is a dictionary of field-value
        pairs of a valid lexicon entry annotation. Keys are the names of the
        annotated fields ('tag', 'root', 'morphophonemics', 'features',
        'is_compound'), values are the annotated values for the respective
        field.
  """
  circumflex = {
      "â": "a",
      "î": "i",
      "û": "u",
  }

  def _normalize_entry(entry):
    entry["tag"] = entry["tag"].upper()
    entry["is_compound"] = entry["is_compound"].lower() == "true"
    entry["root"] = _format_root(entry["root"], entry["tag"])

    for field in ("morphophonemics", "features"):
      entry[field] = "" if entry[field] == "~" else entry[field]

    return entry

  def _root_has_circumflex(entry):
    return any(c in entry["root"] for c in circumflex.keys())

  def _make_entry(entry):
    fields_to_check = ("root", "morphophonemics")
    field_and_chars = itertools.product(fields_to_check, circumflex.items())
    normalized = entry.copy()

    for field, (with_, without) in field_and_chars:
      normalized[field] = normalized[field].replace(with_, without)

    return normalized

  entries[:] = list(map(_normalize_entry, entries))
  new_entries = [_make_entry(e) for e in entries if _root_has_circumflex(e)]
  entries.extend(new_entries)


def _cross_classify(entries):
  """Cross-classifies lexicon entry annotations across parts of speech.

  This function adds a new lexicon entry annotation by just rewriting its tag
  for each part-of-speech that is defined in the CROSS_CLASSIFY_AS dictionary
  of //morphotactics_compiler/lexicon/tags.py.

  While cross-classifying lexicon entry annotations required (or optional)
  features are removed, if required (or optional) features defined for the
  target part-of-speech in REQUIRED_FEATURES and OPTIONAL_FEATURES dictionaries
  of //morphotactics_compiler/lexicon/tags.py does not match the ones that are
  defined for the source part-of-speech.

  Args:
    entries: list of dict(str->str), each item is a dictionary of field-value
        pairs of a valid lexicon entry annotation. Keys are the names of the
        annotated fields ('tag', 'root', 'morphophonemics', 'features',
        'is_compound'), values are the annotated values for the respective
        field.
  """
  def _new_features(old_features, old_tag, new_tag):
    if new_tag == "NOMP-CASE-BARE":
      return "+[PersonNumber=A3sg]+[Possessive=Pnon]+[Case=Bare]"

    old_required = tags.REQUIRED_FEATURES[old_tag]
    new_required = tags.REQUIRED_FEATURES[new_tag]

    if (old_required is not None and old_required == new_required):
      return old_features

    old_optional = tags.OPTIONAL_FEATURES[old_tag]
    new_optional = tags.OPTIONAL_FEATURES[new_tag]

    if (old_optional is not None and old_optional == new_optional):
      return old_features

    return ""

  def _make_entry(entry, old_tag, new_tag):
    new_entry = entry.copy()
    new_entry["tag"] = new_tag
    new_entry["root"] = _format_root(new_entry["root"], new_tag)
    new_entry["features"] = _new_features(entry["features"], old_tag, new_tag)
    return new_entry

  def _new_entries(entry):
    old_tag = entry["tag"]
    new_tags = tags.CROSS_CLASSIFY_AS[old_tag]
    args = itertools.product([entry], [old_tag], new_tags)
    yield from (_make_entry(*a) for a in args)

  new_entries = list(itertools.chain.from_iterable(map(_new_entries, entries)))
  entries.extend(new_entries)


def _rule_input(entry):
  """Returns the input label of a rewrite rule.

  Generated input label has the form '(Root[Tag]+[Cat1=Val_x]...+[Catn=Val_y]'
  (e.g. '(dümdüz[JJ]+[Emphasis=True]').

  Args:
    entry: dict(str->str), field-value pairs of a valid lexicon entry
        annotation. Keys are the names of the annotated fields ('tag', 'root',
        'morphophonemics', 'features', 'is_compound'), values are the annotated
        values for the respective field.
  """
  root = entry["root"]
  tag = tags.OUTPUT_AS[entry["tag"]]
  features = entry["features"]
  return f"({root}[{tag}]{features}"


def _rule_output(entry):
  """Returns the output label of a rewrite rule.

  If lexicon annotation entry has morphophonemics annotated, then it is used
  as the output label. Otherwise, lowercase normalized root form is used as the
  output label.

  Args:
    entry: dict(str->str), field-value pairs of a valid lexicon entry
        annotation. Keys are the names of the annotated fields ('tag', 'root',
        'morphophonemics', 'features', 'is_compound'), values are the annotated
        values for the respective field.
  """
  if entry["morphophonemics"]:
    return entry["morphophonemics"]

  return _lower(entry["root"])


def _create_rewrite_rule(entry):
  """Creates a rewrite rule object from the lexicon entry annotation.

  Args:
    entry: dict(str->str), field-value pairs of a valid lexicon entry
        annotation. Keys are the names of the annotated fields ('tag', 'root',
        'morphophonemics', 'features', 'is_compound'), values are the annotated
        values for the respective field.

  Returns:
    rule_pb2.RewriteRule, rewrite rule object that defines a state transition
    arc of the compiled morphocatics FST.
  """
  rule = rule_pb2.RewriteRule()
  rule.from_state = common.START_STATE
  rule.to_state = entry["tag"]
  rule.input = _rule_input(entry)
  rule.output = _rule_output(entry)
  return rule


def parse(entries):
  """Generates rewrite rules from the lexicon entry annotations source file.

  Note that this function assumes all input entries are valid, meaning that
  they should be first validated with //src/analyzer/lexicon/validator.py.

  Args:
    entries: list of dict(str->str), each item is a dictionary of field-value
        pairs of a valid lexicon entry annotation. Keys are the names of the
        annotated fields ('tag', 'root', 'morphophonemics', 'features',
        'is_compound'), values are the annotated values for the respective
        field.

  Returns:
    rule_pb2.RewriteRuleSet, array of rewrite rule objects that defines a
    subset of the state transition arcs of the compiled morphocatics FST.
  """
  _normalize(entries)
  _cross_classify(entries)
  state_entries = [e for e in entries if e["tag"] in tags.FST_STATES]
  rule_set = rule_pb2.RewriteRuleSet()
  rule_set.rule.extend(map(_create_rewrite_rule, state_entries))
  return rule_set
