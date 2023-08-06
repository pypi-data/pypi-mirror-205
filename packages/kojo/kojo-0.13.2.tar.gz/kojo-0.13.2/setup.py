#!/usr/bin/env python

from distutils.core import setup

setup(
    name="kojo",
    packages=["kojo"],
    version="0.13.2",
    license="GNU GPLv3",
    description="A library to transform data through a pipeline",
    author="Olaf Schneider",
    author_email="mail@olafschneider.com",
    url="https://gitlab.com/filchos/kojo",
    download_url="https://gitlab.com/filchos/kojo/-/archive/0.13.2/kojo-0.13.2.tar.gz",
    install_requires=["jsonschema"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)
