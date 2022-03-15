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

import os
import setuptools

_README_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "README.md",
)

with open(_README_PATH, encoding='utf-8') as f:
  long_description = f.read()


setuptools.setup(
    name="turkish-morphology",
    version="1.2.5",
    description="Turkish Morphology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/google-research/turkish-morphology",
    download_url=("https://github.com/google-research/turkish-morphology/"
                  "releases"),
    license="Apache 2.0",
    packages=setuptools.find_packages(),
    package_data={
        "turkish_morphology": [
            "../external/org_openfst/pywrapfst.so",
            "../src/analyzer/bin/turkish.far",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Turkish",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=["absl-py", "protobuf"],
    python_requires='>=3.9',
)
