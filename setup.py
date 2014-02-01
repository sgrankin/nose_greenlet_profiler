#!/usr/bin/env python
from ez_setup import use_setuptools
use_setuptools()

import sys
from setuptools import setup, Extension, find_packages

long_description = open('README.md').read()
try:
  import pypandoc
  long_description = pypandoc.convert(long_description, 'rst', format='md')
except:
  pass

setup(
  name='nose_greenlet_profiler',
  version='1.0.1',

  description='GreenletProfiler plugin for Nose',
  author='Sergey Grankin',
  url='https://github.com/sgrankin/nose_greenlet_profiler',
  long_description = long_description,
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development',
  ],

  packages=find_packages(),

  install_requires=[
    'GreenletProfiler',
    'nose>=1.0',
  ],
  zip_safe=False,
  test_suite='nose.collector',
  tests_require=[
    'gevent',
  ],

  include_package_data=True,
  entry_points={
    'nose.plugins.0.10': [
      'nose_greenlet_profiler = nose_greenlet_profiler:Profile',
    ]
  },
)
