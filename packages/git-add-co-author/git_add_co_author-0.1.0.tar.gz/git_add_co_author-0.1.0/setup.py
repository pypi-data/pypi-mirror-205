# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_add_co_author']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.29.0,<3.0.0']

setup_kwargs = {
    'name': 'git-add-co-author',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Git Add Co Author\n\n## Description\n\nThis is a simple script to add co-authors to your git commits. It will add the co-author to the commit message.\n\n## Installation\n\n1. Install the package using pip\n```bash\npip install git-add-co-author\n```\n\n2. Obtain a token from GitHub\n\n3. Configure the token \n\n```bash\npython -m git_add_co_author --token <token>\n```\n\n## Usage\n\n\n```bash\npython -m git_add_co_author sansyrox\n```\n',
    'author': 'Sanskar Jethi',
    'author_email': 'sansyrox@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
