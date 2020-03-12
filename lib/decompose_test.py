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

"""Tests for lib.decompose."""

from lib import analysis_pb2
from lib import decompose

from absl.testing import absltest
from absl.testing import parameterized
from google.protobuf import text_format


class HumanReadableAnalysisTest(parameterized.TestCase):

  @parameterized.named_parameters([
      {
          "testcase_name":
              "SingleInflectionalGroupsWithProperFeature",
          "human_readable":
              ("(araba[NN]+lAr[PersonNumber=A3pl]+[Possessive=Pnon]"
               "+DA[Case=Loc])+[Proper=True]"),
          "expected_pbtxt":
              """
              ig {
                pos: 'NN'
                root {
                  morpheme: 'araba'
                }
                inflection {
                  feature {
                    category: 'PersonNumber'
                    value: 'A3pl'
                  }
                  meta_morpheme: 'lAr'
                }
                inflection {
                  feature {
                    category: 'Possessive'
                    value: 'Pnon'
                  }
                }
                inflection {
                  feature {
                    category: 'Case'
                    value: 'Loc'
                  }
                  meta_morpheme: 'DA'
                }
                proper: true
              }""",
      },
      {
          "testcase_name":
              "SingleInflectionalGroupsWithoutProperFeature",
          "human_readable":
              ("(araba[NN]+lAr[PersonNumber=A3pl]+[Possessive=Pnon]"
               "+DA[Case=Loc])"),
          "expected_pbtxt":
              """
              ig {
                pos: 'NN'
                root {
                  morpheme: 'araba'
                }
                inflection {
                  feature {
                    category: 'PersonNumber'
                    value: 'A3pl'
                  }
                  meta_morpheme: 'lAr'
                }
                inflection {
                  feature {
                    category: 'Possessive'
                    value: 'Pnon'
                  }
                }
                inflection {
                  feature {
                    category: 'Case'
                    value: 'Loc'
                  }
                  meta_morpheme: 'DA'
                }
              }""",
      },
      {
          "testcase_name":
              "MultipleInflectionalGroupsWithProperFeature",
          "human_readable":
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "expected_pbtxt":
              """
              ig {
                pos: 'VB'
                root {
                  morpheme: 'yaşa'
                }
                inflection {
                  feature {
                    category: 'Polarity'
                    value: 'Pos'
                  }
                }
              }
              ig {
                pos: 'NOMP'
                derivation {
                  feature {
                    category: 'Derivation'
                    value: 'PastNom'
                  }
                  meta_morpheme: 'DHk'
                }
                inflection {
                  feature {
                    category: 'PersonNumber'
                    value: 'A3pl'
                  }
                  meta_morpheme: 'lAr'
                }
                inflection {
                  feature {
                    category: 'Possessive'
                    value: 'P1sg'
                  }
                  meta_morpheme: 'Hm'
                }
                inflection {
                  feature {
                    category: 'Case'
                    value: 'Abl'
                  }
                  meta_morpheme: 'NDAn'
                }
                inflection {
                  feature {
                    category: 'Copula'
                    value: 'PresCop'
                  }
                }
                inflection {
                  feature {
                    category: 'PersonNumber'
                    value: 'V3pl'
                  }
                }
                proper: false
              }""",
      },
      {
          "testcase_name":
              "MultipleInflectionalGroupsWithoutProperFeature",
          "human_readable":
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])"),
          "expected_pbtxt":
              """
              ig {
                pos: 'VB'
                root {
                  morpheme: 'yaşa'
                }
                inflection {
                  feature {
                    category: 'Polarity'
                    value: 'Pos'
                  }
                }
              }
              ig {
                pos: 'NOMP'
                derivation {
                  feature {
                    category: 'Derivation'
                    value: 'PastNom'
                  }
                  meta_morpheme: 'DHk'
                }
                inflection {
                  feature {
                    category: 'PersonNumber'
                    value: 'A3pl'
                  }
                  meta_morpheme: 'lAr'
                }
                inflection {
                  feature {
                    category: 'Possessive'
                    value: 'P1sg'
                  }
                  meta_morpheme: 'Hm'
                }
                inflection {
                  feature {
                    category: 'Case'
                    value: 'Abl'
                  }
                  meta_morpheme: 'NDAn'
                }
                inflection {
                  feature {
                    category: 'Copula'
                    value: 'PresCop'
                  }
                }
                inflection {
                  feature {
                    category: 'PersonNumber'
                    value: 'V3pl'
                  }
                }
              }""",
      },
  ])
  def test_success(self, human_readable, expected_pbtxt):
    actual = decompose.human_readable_analysis(human_readable)
    expected = text_format.Parse(expected_pbtxt, analysis_pb2.Analysis())
    self.assertEqual(expected, actual)

  @parameterized.named_parameters([
      {
          "testcase_name": "EmptyHumanReadable",
          "human_readable": "",
          "message": "Human-readable analysis is empty.",
      },
      {
          "testcase_name": "HasNoValidIgs",
          "human_readable": "foo",
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "MissingPartOfSpeechTagInFirstIg",
          "human_readable":
              ("(yaşa+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "MissingPartOfSpeechTagInDerivationIg",
          "human_readable":
              ("(yaşa[VB]+[Polarity=Pos])(-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "MissingRootInFirstIg",
          "human_readable":
              ("([VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "MissingDerivationMorpheme",
          "human_readable":
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "MissingFeatureCategory",
          "human_readable":
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "MissingFeatureValue",
          "human_readable":
              ("(yaşa[VB]+[Polarity=])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "MissingDerivationDelimiter",
          "human_readable":
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "MissingInflectionDelimiter",
          "human_readable":
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop][PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "MissingFeatureCategoryValueDelimiter",
          "human_readable":
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[DerivationPastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "UnbalancedParanthesis",
          "human_readable":
              ("(yaşa[VB]+[Polarity=Pos])[NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
      {
          "testcase_name": "UnbalancedBrackets",
          "human_readable":
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
          "message": "Human-readable analysis is ill-formed",
      },
  ])
  def test_raises_exception(self, human_readable, message):
    with self.assertRaisesRegexp(decompose.IllformedHumanReadableAnalysisError,
                                 message):
      decompose.human_readable_analysis(human_readable)


if __name__ == "__main__":
  absltest.main()
