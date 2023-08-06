# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['catgpt']

package_data = \
{'': ['*']}

install_requires = \
['codefast>=23.4.18,<24.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'sseclient-py>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'catgpt',
    'version': '0.0.1',
    'description': 'A simple cli tool to generate text using GPT-turbo',
    'long_description': None,
    'author': 'tom',
    'author_email': 'tom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
