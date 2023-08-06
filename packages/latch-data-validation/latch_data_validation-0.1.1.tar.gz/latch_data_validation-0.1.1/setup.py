# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latch_data_validation']

package_data = \
{'': ['*']}

install_requires = \
['opentelemetry-api>=1.15.0,<2.0.0']

setup_kwargs = {
    'name': 'latch-data-validation',
    'version': '0.1.1',
    'description': 'Data validation for latch python backend services',
    'long_description': '# python-data-validation\n',
    'author': 'Max Smolin',
    'author_email': 'max@latch.bio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
