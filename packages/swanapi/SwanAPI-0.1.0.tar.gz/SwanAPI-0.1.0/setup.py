# -*- coding: utf-8 -*-

"""
@author: cunyue
@software: PyCharm
@file: setup.py
@time: 2023/5/1 02:07
@describe:
打包文件
"""

from setuptools import setup, find_packages

VERSION = '0.1.0'
setup(
    name='SwanAPI',  # package name
    version=VERSION,  # package version
    description='swan-api',  # package description
    packages=find_packages(),
    zip_safe=False,
)
