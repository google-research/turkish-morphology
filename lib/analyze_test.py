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

"""Tests for lib.analyze."""

from lib import analyze

from absl.testing import absltest
from absl.testing import parameterized


class SurfaceFormTest(parameterized.TestCase):

  @parameterized.named_parameters([
      {
          "testcase_name":
              "WordWithAsciiCharacters",
          "surface_form":
              "evdeki",
          "expected": [
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([JJ]-ki[Derivation=Rel])+[Proper=False]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([JJ]-ki[Derivation=Rel])+[Proper=True]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([NOMP]-ki[Derivation=Rel]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Bare]+[Copula=PresCop]"
               "+[PersonNumber=V3pl])+[Proper=False]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([NOMP]-ki[Derivation=Rel]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Bare]+[Copula=PresCop]"
               "+[PersonNumber=V3pl])+[Proper=True]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([NOMP]-ki[Derivation=Rel]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Bare]+[Copula=PresCop]"
               "+[PersonNumber=V3sg])+[Proper=False]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([NOMP]-ki[Derivation=Rel]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Bare]+[Copula=PresCop]"
               "+[PersonNumber=V3sg])+[Proper=True]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([NOMP]-ki[Derivation=Rel]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Nom]+[Copula=PresCop]"
               "+[PersonNumber=V3pl])+[Proper=False]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([NOMP]-ki[Derivation=Rel]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Nom]+[Copula=PresCop]"
               "+[PersonNumber=V3pl])+[Proper=True]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([NOMP]-ki[Derivation=Rel]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Nom]+[Copula=PresCop]"
               "+[PersonNumber=V3sg])+[Proper=False]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([NOMP]-ki[Derivation=Rel]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Nom]+[Copula=PresCop]"
               "+[PersonNumber=V3sg])+[Proper=True]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([PRF]-ki[Derivation=Pron]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Bare])+[Proper=False]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([PRF]-ki[Derivation=Pron]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Bare])+[Proper=True]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([PRF]-ki[Derivation=Pron]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Nom])+[Proper=False]"),
              ("(ev[NN]+[PersonNumber=A3sg]+[Possessive=Pnon]+DA[Case=Loc])"
               "([PRF]-ki[Derivation=Pron]+[PersonNumber=A3sg]"
               "+[Possessive=Pnon]+[Case=Nom])+[Proper=True]"),
          ]
      },
      {
          "testcase_name":
              "WordWithTurkishSpecificCharacters",
          "surface_form":
              "yaşadıklarımdan",
          "expected": [
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=False]"),
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])+[Proper=True]"),
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3sg])+[Proper=False]"),
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3sg])+[Proper=True]"),
              ("(yaşa[VB]+[Polarity=Pos])([VN]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl])"
               "+[Proper=False]"),
              ("(yaşa[VB]+[Polarity=Pos])([VN]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl])"
               "+[Proper=True]"),
          ],
      },
      {
          "testcase_name": "AnalyzeWithoutProperFeature",
          "surface_form": "yaşadıklarımdan",
          "expected": [
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3pl])"),
              ("(yaşa[VB]+[Polarity=Pos])([NOMP]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]"
               "+[Copula=PresCop]+[PersonNumber=V3sg])"),
              ("(yaşa[VB]+[Polarity=Pos])([VN]-DHk[Derivation=PastNom]"
               "+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl])"),
          ],
          "use_proper_feature": False,
      },
  ])
  def test_success(self, surface_form, expected, use_proper_feature=True):
    actual = analyze.surface_form(surface_form,
                                  use_proper_feature=use_proper_feature)
    self.assertListEqual(expected, actual)

  @parameterized.named_parameters([
      {
          "testcase_name": "EmptyWord",
          "surface_form": "",
      },
      {
          "testcase_name": "InvalidWord",
          "surface_form": "foo",
      },
  ])
  def test_failure(self, surface_form):
    actual = analyze.surface_form(surface_form)
    self.assertListEqual([], actual)


if __name__ == "__main__":
  absltest.main()
