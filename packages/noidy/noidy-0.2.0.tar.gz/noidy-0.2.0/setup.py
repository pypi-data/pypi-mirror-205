# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noidy']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['noid = noidy.__main__:main']}

setup_kwargs = {
    'name': 'noidy',
    'version': '0.2.0',
    'description': 'NOID generator in python with JSON persistence.',
    'long_description': None,
    'author': 'datadavev',
    'author_email': '605409+datadavev@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
