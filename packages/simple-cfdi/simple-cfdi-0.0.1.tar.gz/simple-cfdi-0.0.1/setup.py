#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Copyright  2023 Alexis Lopez Zubieta
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-cfdi",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Alexis Lopez Zubieta",
    author_email="alexis.lopez@augetec.com",
    description="CFDI document manipulation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AugeTec/simple-cfdi",
    project_urls={
        "Bug Tracker": "https://github.com/AugeTec/pycfdi/issues",
        "Source Code": "https://github.com/AugeTec/pycfdi",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    install_requires=[
        "xsdata",
    ],
    python_requires=">=3.6",
    package_dir={"simple_cfdi": "simple_cfdi"},
)
