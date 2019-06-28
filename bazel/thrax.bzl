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

# Experimental Bazel extension for compiling Thrax grammars.
#
# This macro is very brittle and makes undesirable assumptions. Among other
# shortcomings, it will only work with grammars that use local (or relative)
# imports, and it requires all transitive dependencies to be listed in deps.
def grm_compile(name, src=None, deps=[]):
    thraxcompiler = "@thrax//:thraxcompiler"

    if not src:
        src = name + ".grm"

    native.genrule(
        name = name + "_grm_compile",
        srcs = [src] + deps,
        outs = [name + ".far"],
        tools = [thraxcompiler],
        cmd = """
              for f in $(SRCS); do
                if [ ! -f $(@D)/$$(basename $$f) ]; then
                  cp $$f $(@D)
                fi
              done &&
              $(location %s) \
                --input_grammar=$$(basename $(location %s)) \
                --indir=$(@D) \
                --output_far=$@ \
                --print_rules=false
              """ % (thraxcompiler, src),
    )

# Experimental Bazel extension for running Thrax grammar tests.
#
# This macro assumes that all test data files are in a subdirectory
# named 'testdata' relative to the location of the far file, which
# is the base_path.
def grm_test(name, far_file, test_file, base_path):
    testdata_dir = "testdata/"

    native.cc_test(
        name = name,
        size = "small",
        args = [
            "--far=" + base_path + far_file,
            "--test_file=" + base_path + testdata_dir + test_file
        ],
        data = [
              far_file,
              testdata_dir + test_file,
        ],
        deps = [
            "@language_resources//utils:grm_tester_lib"
        ],
    )
