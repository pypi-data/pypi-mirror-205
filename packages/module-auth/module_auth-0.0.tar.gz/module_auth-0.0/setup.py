# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 06:21:25 2023

@author: nehayerpula
"""
from setuptools import setup
setup(name='module_auth',
      version='0.0',
      description='jwt authentication',
      packages=['module_auth'],
      author_email='nehayerpula@rangam.com',
      install_requires = ['urllib3'],
      zip_safe=False)