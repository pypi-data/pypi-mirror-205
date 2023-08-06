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
    'version': '0.4.0',
    'description': '',
    'long_description': '# Git Add Co-Author\n\n## Demo\n![git-add-co-author](https://user-images.githubusercontent.com/29942790/235257344-93578bf7-104a-46b7-9785-ef6620a019b5.gif)\n\n\n\n## Overview\n\nGit Add Co-Author is a simple Python script that allows you to easily add co-authors to your Git commits, ensuring proper credit is given to all contributors involved in the development process. This can be particularly useful for open-source projects, where multiple contributors are working together, or for pair programming sessions where two developers contribute to the same commit.\n\n## Installation\n\n1. Install the package using pip:\n\n```bash\npip install git-add-co-author\n```\n\n2. Obtain a personal access token from GitHub. You can generate one by following the instructions in the [GitHub documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).\n\n3. Configure the script with your GitHub token:\n\n```bash\npython -m git_add_co_author --token <your_token>\n```\n\n## Usage\n\nTo add a co-author to your commit, simply run the script with the co-author\'s GitHub username:\n\n```bash\npython -m git_add_co_author --username <co_author_username>\n```\n\nFor example:\n\n```bash\npython -m git_add_co_author sansyrox\n```\n\nIf you do not want to authorize a token, you can add the co-author\'s name and email address directly:\n\n```bash\npython -m git_add_co_author --name "John Doe" --email "john.doe@example.com"\n```\n\n### Optional Configuration\n\nI alias this command as `alias gac="python -m git_add_co_author --username"` in my `.zshrc` file, so I can simply run `gac <co_author_username>` to add a co-author to my commit.\n\n## Rationale\n\nThe motivation behind creating this script is to provide an easy way to give credit to contributors in various situations:\n\n- In open-source projects, when a pull request (PR) is closed without merging but the idea or code is later implemented.\n- During pair programming sessions, where two or more developers work together on a single commit.\n\nExisting solutions were either too complicated or didn\'t work as expected, so Git Add Co-Author was developed as a simple, easy-to-use alternative.\n\n## License\n\nThis project is licensed under the MIT License.\n',
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
