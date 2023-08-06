# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['simplecm']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.3,<2.0.0', 'scipy>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'simplecm',
    'version': '0.1.0',
    'description': 'Helps you calculate basic manufacturing statistics',
    'long_description': None,
    'author': 'David Hinojosa',
    'author_email': 'hynack@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
