# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safenote']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'safenote',
    'version': '0.1.5',
    'description': 'SafeNote (Safe Notebook) is a tool for injecting your secrets into Jupyter notebooks environment safer and easier.',
    'long_description': '<img src="https://imagedelivery.net/Dr98IMl5gQ9tPkFM5JRcng/b4e3b105-8503-43ac-9116-f51e401b6b00/HD" alt="Cover"/>',
    'author': 'Lingxi Li',
    'author_email': 'lilingxi01@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://safenote.lingxi.li/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
