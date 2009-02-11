#!/usr/bin/env python

from distutils.core import setup

setup(name='egmont-gateway',
      version='0.3',
      description='Connect to the Egmont network',
      author='Daniel Schierbeck',
      author_email='daniel.schierbeck@gmail.com',
      url='http://github.com/dasch/egmont-gateway',
      packages=['egmont'],
      data_files=[('share/egmont-gateway/glade', ['data/egmont.glade']),
                  ('share/applications', ['data/egmont-gateway.desktop'])],
      scripts=['egmont-gateway'],
     )

