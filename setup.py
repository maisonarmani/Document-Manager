# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from setuptools import setup, find_packages
import re, ast

# get version from __version__ variable in document_manager/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('./requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

with open('document_manager/__init__.py', 'rb') as f:
	version = str(ast.literal_eval(_version_re.search(
		f.read().decode('utf-8')).group(1)))

setup(
	name='document_manager',
	version=version,
	description='This is to manage documents',
	author='masonarmani',
	author_email='masonarmani38@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
