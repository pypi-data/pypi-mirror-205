# -*- coding: utf8 -*-
from setuptools import setup
from os import path
import io
abs_path = path.abspath(path.dirname(__file__))
with io.open(path.join(abs_path, 'README.md'), encoding='utf-8') as f:
    readme_data = f.read()

setup(
    name='with_timeout',
    py_modules=['with_timeout'],
    version='0.0.4',
    description='模拟requests的timeout参数，使任意函数都拥有超时跳出的功能，防止访问超时阻塞影响代码的运行',
    author='Jeffrey Yang',
    author_email='snjyor@163.com',
    url='https://github.com/snjyor/with_timeout',
    install_requires=[
        'beautifulsoup4'
    ],
    license='MIT',
    long_description=readme_data,
    long_description_content_type='text/markdown',
)