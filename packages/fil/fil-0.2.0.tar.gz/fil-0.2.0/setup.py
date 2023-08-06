# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fil']
install_requires = \
['safer>=4.5.0,<5.0.0']

setup_kwargs = {
    'name': 'fil',
    'version': '0.2.0',
    'description': '🏺 Read/write JSON, TOML, ... files 🏺',
    'long_description': '# fil\n🏺 Read, write files (JSON, TOML, ...) 🏺\n',
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
