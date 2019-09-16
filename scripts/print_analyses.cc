// Copyright 2019 The Google Research Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// \file
// Prints all possible morphological analysis strings for an input Turkish word.

#include <deque>
#include <iostream>
#include <string>
#include <vector>

#include "absl/strings/str_join.h"
#include "fst/arcsort.h"
#include "fst/compose.h"
#include "fst/project.h"
#include "fst/symbol-table.h"
#include "fst/vector-fst.h"
#include "thrax/grm-manager.h"

DEFINE_string(word, "", " required: word to morphologically analyze.");
DEFINE_string(far_path, "",
              " optional: path to the FAR file that contains the Turkish"
              " morphological analyzer FST.");
DEFINE_string(fst_name, "turkish_morphological_analyzer",
              " optional: name of the rule from the FAR file that defines"
              " Turkish morphological analyzer FST.");

namespace {

using fst::ArcIterator;
using fst::StdArc;
using fst::StdFst;
using fst::SymbolTable;
using std::string;
using Analysis = std::deque<string>;
using Compiler = fst::StringCompiler<StdArc>;
using MutableTransducer = fst::VectorFst<StdArc>;
using Transducer = fst::Fst<StdArc>;

std::vector<Analysis> Analyses(const MutableTransducer& output,
                               StdArc::StateId state) {
  std::vector<Analysis> analyses;
  if (state == fst::kNoStateId) return analyses;

  for (ArcIterator<StdFst> aitr(output, state); !aitr.Done(); aitr.Next()) {
    const StdArc& arc = aitr.Value();

    auto add_analysis_with_arc = [&](Analysis* analysis) {
      if (arc.ilabel != 0) {
        const SymbolTable* symbol_table = output.InputSymbols();
        if (!symbol_table) {
          LOG(FATAL) << "Cannot load symbols table of output FST";
        }
        const string symbol = symbol_table->Find(arc.ilabel);
        if (symbol.empty()) {
          LOG(FATAL) << "Cannot find the symbol for the label '" << arc.ilabel
                     << "' in symbols table of output FST";
        }
        analysis->push_front(symbol);
      }
      analyses.push_back(*analysis);
    };

    if (output.Final(arc.nextstate) != fst::StdVectorFst::Weight::Zero()) {
      add_analysis_with_arc(new Analysis());
      continue;
    }

    for (auto& analysis : Analyses(output, arc.nextstate)) {
      add_analysis_with_arc(&analysis);
    }
  }
  return analyses;
}

}  // namespace

int main(int argc, char** argv) {
  SET_FLAGS(argv[0], &argc, &argv, true);

  string far_path = FLAGS_far_path;
  if (far_path.empty()) {
    far_path = argv[0];
    far_path += ".runfiles/turkish_morphology/src/analyzer/bin/turkish.far";
  }

  thrax::GrmManagerSpec<StdArc> grm_manager;
  if (!grm_manager.LoadArchive(far_path)) {
    LOG(FATAL) << "Cannot load FAR file '" << far_path << "'";
  }

  const Transducer* analyzer = grm_manager.GetFst(FLAGS_fst_name);
  if (!analyzer) {
    LOG(FATAL) << "Unable to get FST '" << FLAGS_fst_name << "' from FAR file"
               << " '" << FLAGS_far_path << "'";
  }

  MutableTransducer input;
  Compiler compiler_(fst::StringTokenType::BYTE);
  if (!compiler_(FLAGS_word, &input)) {
    LOG(FATAL) << "Unable to parse input word '" << FLAGS_word << "' into FST";
  }

  MutableTransducer output;
  fst::ArcSort(&input, fst::StdOLabelCompare());
  fst::Compose(input, *analyzer, &output);
  fst::Project(&output, fst::PROJECT_OUTPUT);

  const std::vector<Analysis>& analyses = Analyses(output, output.Start());
  if (!analyses.empty()) {
    std::vector<string> printables;
    for (const Analysis& analysis : analyses) {
      printables.push_back(absl::StrJoin(analysis, ""));
    }
    std::sort(printables.begin(), printables.end());
    std::cout << "Morphological analyses for the word '" << FLAGS_word
              << "':" << std::endl;
    for (const string& analysis : printables) {
      std::cout << analysis << std::endl;
    }
  } else {
    std::cout << "'" << FLAGS_word << "' is not accepted as a Turkish word"
              << std::endl;
  }

  return 0;
}
