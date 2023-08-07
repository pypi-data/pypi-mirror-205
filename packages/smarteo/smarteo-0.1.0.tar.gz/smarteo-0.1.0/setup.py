# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smarteo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'smarteo',
    'version': '0.1.0',
    'description': 'Interact with the SmartEO API using python',
    'long_description': '# SmartEO SDK for python\n\nThis is a package for interacting with SmartEO API and services using python.\n',
    'author': 'Mads Wilthil',
    'author_email': 'mads.wilthil@aenergi.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
