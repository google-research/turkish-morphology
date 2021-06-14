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
def grm_compile(name, src = None, deps = []):
    thraxcompiler = "@org_opengrm_thrax//:compiler"

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
