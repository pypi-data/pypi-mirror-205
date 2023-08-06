# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fil']
setup_kwargs = {
    'name': 'fil',
    'version': '0.1.0',
    'description': '🏺 Read/write JSON, TOML, ... files 🏺',
    'long_description': '# fil\n🏺 Read, write files (JSON, TOML, ...) 🏺\n',
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
