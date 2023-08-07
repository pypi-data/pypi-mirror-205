# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safenote']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'safenote',
    'version': '0.1.1',
    'description': 'SafeNote (Safe Notebook) is a tool for injecting your secrets into Jupyter notebooks environment safer and easier.',
    'long_description': '',
    'author': 'Lingxi Li',
    'author_email': 'lilingxi01@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lilingxi01/safenote',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
