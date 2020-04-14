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

workspace(name = "google_research_turkish_morphology")

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
http_archive(
    name = "com_google_protobuf",
    sha256 = "a79d19dcdf9139fa4b81206e318e33d245c4c9da1ffed21c87288ed4380426f9",
    strip_prefix = "protobuf-3.11.4",
    urls = [
        "https://github.com/protocolbuffers/protobuf/archive/v3.11.4.tar.gz",
    ],
)

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

# Abseil Python common libraries.
http_archive(
    name = "io_abseil_py",
    sha256 = "603febc9b95a8f2979a7bdb77d2f5e4d9b30d4e0d59579f88eba67d4e4cc5462",
    strip_prefix = "abseil-py-pypi-v0.9.0",
    urls = [
        "https://github.com/abseil/abseil-py/archive/pypi-v0.9.0.tar.gz",
    ],
)

# Bazel Python rules.
http_archive(
    name = "rules_python",
    sha256 = "aa96a691d3a8177f3215b14b0edc9641787abaaa30363a080165d06ab65e1161",
    urls = [
        "https://github.com/bazelbuild/rules_python/releases/download/0.0.1/rules_python-0.0.1.tar.gz",
    ],
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

# gRpc (only used for detecting and configuring local Python).
http_archive(
    name = "com_github_grpc_grpc",
    sha256 = "4cbce7f708917b6e58b631c24c59fe720acc8fef5f959df9a58cdf9558d0a79b",
    strip_prefix = "grpc-1.28.1",
    urls = [
        "https://github.com/grpc/grpc/archive/v1.28.1.tar.gz",
    ],
)

load(
    "@com_github_grpc_grpc//third_party/py:python_configure.bzl",
    "python_configure",
)

python_configure(name = "local_config_python")

# Google i18n language resources.
http_archive(
    name = "language_resources",
    sha256 = "95b42c933f34e8444182558eee3f0be15d5ab63cd759a4917034747fdb1dacfd",
    strip_prefix = "language-resources-5dc64ca8441b0e7b6d06fd08933f91452ab384d6",
    urls = [
        "https://github.com/google/language-resources/archive/5dc64ca.tar.gz",
    ],
)

# OpenFst.
http_archive(
    name = "openfst",
    build_file = "@//third_party:openfst.BUILD",
    sha256 = "eb57e469201b4813479527f0d4661ce3459e282ff7af643613ebe3ea71c79f27",
    strip_prefix = "openfst-1.7.2",
    urls = [
        "https://github.com/mjansche/openfst/archive/1.7.2.tar.gz",
    ],
)

# Thrax.
http_archive(
    name = "thrax",
    build_file = "@//third_party:thrax.BUILD",
    sha256 = "40caa83dc083abdb1b8603a7f74eccb6348877279ab37296a68a570469e3ecfb",
    strip_prefix = "thrax-c65fb3d51f9bd0299503f3289a124f52c3431eeb",
    urls = [
        "https://github.com/mjansche/thrax/archive/c65fb3d.tar.gz",
    ],
)
