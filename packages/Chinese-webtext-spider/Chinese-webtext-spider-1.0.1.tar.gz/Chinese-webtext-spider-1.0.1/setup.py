#!/usr/bin/env python
from io import open
from setuptools import setup, find_packages
setup(
    name='Chinese-webtext-spider',
    version='1.0.1',
    description='a package for crawling chinese webtext',
    long_description='一个用于爬取网络中文文本的爬虫工具',
    author='ZhaoRunSong',
    author_email='1398915234@qq.com',
    license='Apache License 2.0',
    url='https://github.com/1azybug/chinese-webtext-spider',
    download_url='https://github.com/1azybug/chinese-webtext-spider/master.zip',
    packages=find_packages(),
    install_requires=['requests','torch','transformers']
)