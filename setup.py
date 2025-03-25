#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import setuptools
import os
import re
import glob
import shutil

def read_file_as_utf8(filepath):
    with open(filepath, encoding="utf-8") as fh:
        return fh.read()


def main(base_dir):

    doc_dir="share/doc/nerd-dictation"
    fn="nerd-dictation.py"
    doc_list=[(doc_dir,list(filter(re.compile(r'.*rst').match, os.listdir("./"))))]
    for ex in glob.glob("examples/*/"):
        doc_list.append((os.path.join(doc_dir,ex), [os.path.join(ex,fn)]))

    if os.geteuid()!=0 and os.name=="posix":
        config_dir=os.path.join(os.path.expanduser("~"),".config/nerd-dictation")
        if not os.path.isdir(config_dir):
            os.makedirs(config_dir)
        shutil.copy("examples/default/nerd-dictation.py",config_dir)
        # For cross-platform assistance, see: (pypi: appdirs) (github: platformdirs)
        # For root install, first support /etc/nerd-dictation

    setuptools.setup(
        name="nerd-dictation",
        version="0.0.0",
        maintainer="Campbell Barton",
        maintainer_email="ideasman42@gmail.com",
        description="Offline Speech to Text for Desktop",
        long_description=read_file_as_utf8("readme.rst"),
        long_description_content_type="text/x-rst",
        url="https://github.com/ideasman42/nerd-dictation",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Topic :: Office :: Productivity",
            "Topic :: Accessibility :: Voice",
            "Operating System :: POSIX :: Linux",
            "License :: OSI Approved :: GPL v3.0",
        ],
        scripts=["nerd-dictation"],
        data_files=doc_list,
        packages=[""],
        package_data={"nerd-dictation": [""]},
        install_requires=["vosk"],
        python_requires=">=3.8",
    )


if __name__ == "__main__":
    main(os.path.abspath(os.path.dirname(__file__)))
