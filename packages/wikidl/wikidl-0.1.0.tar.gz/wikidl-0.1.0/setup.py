# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikidl']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.12.2,<5.0.0',
 'psutil>=5.9.5,<6.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'wikidl',
    'version': '0.1.0',
    'description': 'WikiDL is a helpful command-line tool to download Wikipedia dumps.',
    'long_description': '',
    'author': 'Lingxi Li',
    'author_email': 'lilingxi01@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://wikidl.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
