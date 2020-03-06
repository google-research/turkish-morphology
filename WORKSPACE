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

# Python 2/3 compatibility.
http_archive(
    name = "six_archive",
    build_file = "@//third_party:six.BUILD",
    sha256 = "236bdbdce46e6e6a3d61a337c0f8b763ca1e8717c03b369e87a7ec7ce1319c0a",
    strip_prefix = "six-1.14.0",
    urls = [
        "https://pypi.python.org/packages/source/s/six/six-1.14.0.tar.gz",
    ],
)

# Google protocol buffers.
git_repository(
    name = "com_google_protobuf",
    remote = "https://github.com/google/protobuf.git",
    tag = "v3.11.4",
)

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

# Abseil Python common libraries.
git_repository(
    name = "io_abseil_py",
    remote = "https://github.com/abseil/abseil-py.git",
    tag = "pypi-v0.9.0",
)

# Bazel Python rules.
git_repository(
    name = "rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    tag = "0.0.1",
)

# gRpc (only used for detecting and configuring local Python).
git_repository(
    name = "com_github_grpc_grpc",
    remote = "https://github.com/grpc/grpc.git",
    tag = "v1.27.3",
)

load(
    "@com_github_grpc_grpc//third_party/py:python_configure.bzl",
    "python_configure",
)

python_configure(name = "local_config_python")

# Google i18n language resources.
git_repository(
    name = "language_resources",
    commit = "5dc64ca8441b0e7b6d06fd08933f91452ab384d6",
    remote = "https://github.com/google/language-resources.git",
)

# OpenFst.
new_git_repository(
    name = "openfst",
    build_file = "@//third_party:openfst.BUILD",
    remote = "https://github.com/mjansche/openfst.git",
    tag = "1.7.2",
)

# Thrax.
new_git_repository(
    name = "thrax",
    build_file = "@//third_party:thrax.BUILD",
    commit = "c65fb3d51f9bd0299503f3289a124f52c3431eeb",
    remote = "https://github.com/mjansche/thrax.git",
)
