# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'validators',
    'requests'
    ]

setup(name='pixget',
      version='0.1',
      description='Python based pictures download script.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
      ],
      author='Jörg Kubaile',
      author_email='joerg@kubaile.de',
      url='https://github.com/jkubaile/pixget',
      packages=find_packages(),
      test_suite="pixget.tests.test_pixget",
      tests_require=['requests-mock'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points={
          'console_scripts': [
              'pixget=pixget.script:main',
          ],
      }
      )
