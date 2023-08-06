# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['otdrparser']
setup_kwargs = {
    'name': 'otdrparser',
    'version': '0.1.0',
    'description': 'Python library for parsing OTDR files in Telcordia SR-4731 Version 2 format',
    'long_description': None,
    'author': 'Markus Juenemann',
    'author_email': 'markus@juenemann.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
