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

"""Functions to validate lexicon entry annotations."""

import re

from src.analyzer.lexicon import tags


class InvalidLexiconEntryError(Exception):
  """Raised when a lexicon entry is illformed."""


_FEATURE_CATEGORY_VALUE_REGEX = re.compile(
    r"\+\[([A-z0-9]+?)=([A-z0-9]+?)\]")
_FEATURES_REGEX = re.compile(
    r"(?:\+\[[A-z0-9]+?=[A-z0-9]+?\])+")
_REQUIRED_FIELDS = set([
    "tag",
    "root",
    "morphophonemics",
    "features",
    "is_compound",
])


def _tag_of(entry):
  """Returns normalized tag annotation of the entry."""
  return entry["tag"].upper()


def _morphophonemics_of(entry):
  """Returns morphophonemics annotation of the entry."""
  return entry["morphophonemics"]


def _features_of(entry):
  """Returns features annotation of the entry."""
  return entry["features"]


def _is_compound_of(entry):
  """Returns normalized compound annotation of the entry."""
  return entry["is_compound"].lower()


def _category_value_pairs(features):
  """Extracts feature category-value pairs from features annotation string."""
  return [f for f in _FEATURE_CATEGORY_VALUE_REGEX.findall(features) if f]


def _entry_has_required_fields(entry):
  """Checks if entry has all required fields to create a rewrite rule."""
  missing_fields = [f for f in _REQUIRED_FIELDS if f not in entry]

  if missing_fields:
    field_str = ", ".join(sorted(missing_fields))
    raise InvalidLexiconEntryError(
        f"Entry is missing fields: '{field_str}'")


def _entry_field_values_are_not_empty(entry):
  """Checks if all required entry fields have non-empty values."""
  empty_fields = [f for f in _REQUIRED_FIELDS if not entry[f]]

  if empty_fields:
    field_str = ", ".join(sorted(empty_fields))
    raise InvalidLexiconEntryError(
        f"Entry fields have empty values: '{field_str}'")


def _entry_field_values_does_not_contain_infix_whitespace(entry):
  """Checks if entry has single token tag, morphophonemics and feature value."""
  def _has_multi_token_value(field):
    return len(entry[field].split()) != 1

  fields_to_check = ("tag", "morphophonemics", "features")
  multi_token_fields = [f for f in fields_to_check if _has_multi_token_value(f)]

  if multi_token_fields:
    field_str = ", ".join(sorted(multi_token_fields))
    raise InvalidLexiconEntryError(
        f"Entry field values contain whitespace: '{field_str}'")


def _entry_tag_is_valid(entry):
  """Checks if entry tag is valid."""
  tag = _tag_of(entry)

  if tag not in tags.VALID_TAGS:
    raise InvalidLexiconEntryError(
        "Entry 'tag' field has invalid value. It can only be one of the valid"
        " tags that are defined in 'morphotactics_compiler/tags.py'.")


def _entry_compound_annotation_is_valid(entry):
  """Checks if entry compound annotation is valid ('true' or 'false')."""
  compound = _is_compound_of(entry)
  valid_values = ("true", "false")

  if compound not in valid_values:
    raise InvalidLexiconEntryError(
        "Entry 'is_compound' field has invalid value. It can only have the"
        " values 'true' or 'false'.")


def _entry_morphophonemics_annotation_is_valid(entry):
  """Checks if entry has a morphophonemics annotation if it is a compound."""
  compound = _is_compound_of(entry)
  morphophonemics = _morphophonemics_of(entry)

  if compound == "true" and morphophonemics == "~":
    raise InvalidLexiconEntryError(
        "Entry is marked as ending with compounding marker but it is missing"
        " morphophonemics annotation.")


def _entry_features_annotation_is_valid(entry):
  """Checks if entry features annotation is valid (e.g. '+[Cat=Tag]...')."""
  features = _features_of(entry)

  if not (features == "~" or _FEATURES_REGEX.fullmatch(features)):
    raise InvalidLexiconEntryError(
        "Entry features annotation is invalid. Features need to be annotated"
        " as '+[Category_1=Value_x]...+[Category_n=Value_y].")


def _entry_has_required_features(entry):
  """Checks if entry has features if its expected to have required features."""
  features = _features_of(entry)
  tag = _tag_of(entry)
  required = tags.REQUIRED_FEATURES[tag]

  if features == "~" and required:
    raise InvalidLexiconEntryError("Entry is missing required features.")


def _entry_required_features_are_valid(entry):
  """Checks if entry has the expected set of required features."""
  tag = _tag_of(entry)
  required = tags.REQUIRED_FEATURES[tag]

  if not required:
    return

  features = _features_of(entry)
  category_value = _category_value_pairs(features)
  categories, values = zip(*category_value)

  if categories != tuple(required.keys()):
    raise InvalidLexiconEntryError(
        "Entry has invalid required feature category.")

  if any(v not in r for v, r in zip(values, required.values())):
    raise InvalidLexiconEntryError(
        "Entry has invalid required feature value.")


def _entry_optional_features_are_valid(entry):
  """Checks if optional features of the entry are valid."""
  tag = _tag_of(entry)
  optional = tags.OPTIONAL_FEATURES[tag]

  if not optional:
    return

  features = _features_of(entry)
  category_value = _category_value_pairs(features)

  if not all(c in optional and v in optional[c] for c, v in category_value):
    raise InvalidLexiconEntryError("Entry has invalid optional features.")


def _entry_features_are_not_redundant(entry):
  """Checks if entry doesn't have features if its not expected to have any."""
  features = _features_of(entry)
  tag = _tag_of(entry)
  required = tags.REQUIRED_FEATURES[tag]
  optional = tags.OPTIONAL_FEATURES[tag]

  if not (required or optional) and features != "~":
    raise InvalidLexiconEntryError(
        "Entry has features while it is not expected to have any.")


def validate(entry):
  """Raises an exception if the lexicon entry annotation is illformed.

  Args:
    entry: dict(str->str), keys are the names of the annotation fields, values
        are the manual annotations for each respective field.

  Raises:
    InvalidLexiconEntryError: lexicon entry is missing a non-empty required
        annotation field (that are defined in the _REQUIRED_FIELDS list), or
        one of its fields ('tag', 'morphophonemics', 'features') has an
        annotation that contains whitespace, or its features annotation is
        invalid.
  """
  _entry_has_required_fields(entry)
  _entry_field_values_are_not_empty(entry)
  _entry_field_values_does_not_contain_infix_whitespace(entry)
  _entry_tag_is_valid(entry)
  _entry_compound_annotation_is_valid(entry)
  _entry_morphophonemics_annotation_is_valid(entry)
  _entry_features_annotation_is_valid(entry)
  _entry_has_required_features(entry)
  _entry_required_features_are_valid(entry)
  _entry_optional_features_are_valid(entry)
  _entry_features_are_not_redundant(entry)
