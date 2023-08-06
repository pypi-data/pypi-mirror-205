# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factly', 'factly.standard_names']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy>=0.18.0,<0.19.0', 'pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'factly-standard-names',
    'version': '0.1.5',
    'description': '',
    'long_description': 'None',
    'author': 'Factly Labs',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
