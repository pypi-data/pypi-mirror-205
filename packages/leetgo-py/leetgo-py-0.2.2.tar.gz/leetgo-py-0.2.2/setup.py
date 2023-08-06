# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['leetgo_py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'leetgo-py',
    'version': '0.2.2',
    'description': 'Python test utils for leetgo',
    'long_description': None,
    'author': 'j178',
    'author_email': '10510431+j178@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/j178/leetgo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
