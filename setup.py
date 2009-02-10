#!/usr/bin/env python

from distutils.core import setup

setup(name='Egmont Connect',
      version='0.1',
      description='Connect to the Egmont network',
      author='Daniel Schierbeck',
      author_email='daniel.schierbeck@gmail.com',
      url='http://github.com/dasch/egmont-gateway',
      packages=['egmont'],
      data_files=[('share', 'data/egmont.glade')],
     )

