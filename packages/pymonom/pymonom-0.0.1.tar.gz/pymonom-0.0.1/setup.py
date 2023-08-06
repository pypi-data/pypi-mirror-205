# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymonom', 'pymonom.notification']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'pydantic>=1.9.1,<1.10.0', 'pyhumps==3.5.3']

setup_kwargs = {
    'name': 'pymonom',
    'version': '0.0.1',
    'description': 'monom python library test.',
    'long_description': None,
    'author': 'Alejandro Marichal',
    'author_email': 'jamarichal@monom.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
