#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import os
import setuptools
import shutil
import tempfile


def read_file_as_utf8(filepath):
    with open(filepath, encoding="utf-8") as fh:
        return fh.read()


def main(base_dir):
    root_dir = os.path.normpath(os.path.join(base_dir, "..", ".."))

    if not os.path.exists(os.path.join(root_dir, "nerd-dictation")):
        root_dir = base_dir
    CWD = os.getcwd()

    NERD_DICTATION_DST = os.path.join(base_dir, "nerd-dictation")
    README_DST = os.path.join(base_dir, "doc", "readme.rst")
    os.makedirs(os.path.join(base_dir, "doc"), exist_ok=True)

    # Path pairs to copy.
    COPY_PATH_PAIRS = (
        # As this is a single, self contained script, this is all that's needed.
        (os.path.join(root_dir, "nerd-dictation"), NERD_DICTATION_DST),
        (os.path.join(root_dir, "readme.rst"), README_DST),
    )

    if root_dir != base_dir:
        for src, dst in COPY_PATH_PAIRS:
            shutil.copy2(src, dst)

    # `setuptools` expects relative paths.
    NERD_DICTATION_DST = os.path.relpath(NERD_DICTATION_DST, CWD)
    README_DST = os.path.relpath(README_DST, CWD)

    setuptools.setup(
        name="nerd-dictation",
        version="0.0.0",
        maintainer="Campbell Barton",
        maintainer_email="ideasman42@gmail.com",
        description="Offline Speech to Text for Desktop",
        long_description=read_file_as_utf8(README_DST),
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
        data_files=[
            ("nerd-dictation", [NERD_DICTATION_DST, README_DST])
        ],
        packages=[""],
        package_data={"": [NERD_DICTATION_DST, README_DST]},
        include_package_data=True,
        install_requires=["vosk"],
        python_requires=">=3.8",
    )


if __name__ == "__main__":
    main(os.path.abspath(os.path.dirname(__file__)))
