# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpart', 'rpart.DecisionTree-trythis']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'rpart',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Qiushi Yan',
    'author_email': 'qiushi.yann@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
