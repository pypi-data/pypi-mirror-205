# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grafiks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'grafiks',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Anonymous',
    'author_email': 'f-off@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
