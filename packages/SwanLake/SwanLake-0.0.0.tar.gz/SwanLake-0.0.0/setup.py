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

VERSION = '0.0.0'
setup(
    name='SwanLake',  # package name
    version=VERSION,  # package version
    description='swan-lake',  # package description
    packages=find_packages(),
    zip_safe=False,
)
