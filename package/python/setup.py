#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import os
import setuptools
import shutil
import tempfile

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", ".."))

NERD_DICTATION_DST = os.path.join(BASE_DIR, "nerd-dictation")

# Path pairs to copy.
COPY_PATH_PAIRS = (
    # As this is a single, self contained script, this is all that's needed.
    (os.path.join(ROOT_DIR, "nerd-dictation"), NERD_DICTATION_DST),
)


def read_file_as_utf8(filepath):
    with open(filepath, encoding="utf-8") as fh:
        return fh.read()


def main(temp_dir):
    for src, dst in COPY_PATH_PAIRS:
        shutil.copy2(src, dst)

    setuptools.setup(
        name="nerd-dictation",
        version="0.0.0",
        maintainer="Campbell Barton",
        maintainer_email="ideasman42@gmail.com",
        description="Offline Speech to Text for Desktop",
        long_description=read_file_as_utf8(os.path.join(ROOT_DIR, "readme.rst")),
        long_description_content_type="text/x-rst",
        url="https://github.com/ideasman42/nerd-dictation",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Topic :: Office :: Productivity",
            "Topic :: Accessibility :: Voice",
            "Operating System :: POSIX :: Linux",
            "License :: OSI Approved :: GPL v3.0",
        ],
        scripts=[NERD_DICTATION_DST],
        install_requires=["vosk"],
        python_requires=">=3.8",
    )


if __name__ == "__main__":
    # Create a temporary directory as the source location cannot be above this path.
    with tempfile.TemporaryDirectory(prefix="build_", dir=BASE_DIR) as temp_dir:
        main(temp_dir)
