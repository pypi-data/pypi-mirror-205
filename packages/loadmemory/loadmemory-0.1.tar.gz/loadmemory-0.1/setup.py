#!/usr/bin/python3.8+
# -*- coding:utf-8 -*-
import setuptools

setuptools.setup(
    name="loadmemory",
    version="0.1",

    description="tools",
    long_description="tools",
    author="zhouwe1",
    author_email="zhouwei@live.it",
    url="https://github.com/zhouwe1/loadmemory_util",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    package_data={
        'loadmemory': [
            'utils/*',
        ]
    }
)
