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

workspace(name = "turkish_morphology")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load(
    "@bazel_tools//tools/build_defs/repo:git.bzl",
    "git_repository",
    "new_git_repository",
)

# Google protocol buffers.
git_repository(
    name = "com_google_protobuf",
    remote = "https://github.com/google/protobuf.git",
    tag = "v3.9.0",
)

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

# Explicitly import protocol buffer Skylib dependency. Below rule will become
# obsolete once https://github.com/protocolbuffers/protobuf/issues/5178 is
# fixed.
git_repository(
    name = "bazel_skylib",
    remote = "https://github.com/bazelbuild/bazel-skylib.git",
    tag = "0.9.0",
)

# Google Abseil libraries.
git_repository(
    name = "com_google_absl",
    remote = "https://github.com/abseil/abseil-cpp.git",
    tag = "20181200",
)

# Python 2/3 backward compatibility libs.
http_archive(
    name = "six_archive",
    build_file = "@//bazel:six.BUILD",
    sha256 = "d16a0141ec1a18405cd4ce8b4613101da75da0e9a7aec5bdd4fa804d0e0eba73",
    strip_prefix = "six-1.12.0",
    url = "https://files.pythonhosted.org/packages/dd/bf/4138e7bfb757de47d1f4b6994648ec67a51efe58fa907c1e11e350cddfca/six-1.12.0.tar.gz",
)

bind(
    name = "six",
    actual = "@six_archive//:six",
)

# Google i18n language resources.
git_repository(
    name = "language_resources",
    commit = "5dc64ca8441b0e7b6d06fd08933f91452ab384d6",
    remote = "https://github.com/google/language-resources.git",
)

# OpenFst.
new_git_repository(
    name = "openfst",
    build_file = "@//bazel:openfst.BUILD",
    remote = "https://github.com/mjansche/openfst.git",
    tag = "1.7.2",
)

# Thrax.
new_git_repository(
    name = "thrax",
    build_file = "@//bazel:thrax.BUILD",
    commit = "c65fb3d51f9bd0299503f3289a124f52c3431eeb",
    remote = "https://github.com/mjansche/thrax.git",
)

# PyPi dependencies.
git_repository(
    name = "io_bazel_rules_python",
    branch = "master",
    remote = "https://github.com/bazelbuild/rules_python.git",
)

load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

load("@io_bazel_rules_python//python:pip.bzl", "pip_import")

pip_import(
    name = "turkish_morphology_deps",
    requirements = "@turkish_morphology//:requirements.txt",
)

load(
    "@turkish_morphology_deps//:requirements.bzl",
    _install_turkish_morphology_deps = "pip_install",
)

_install_turkish_morphology_deps()
