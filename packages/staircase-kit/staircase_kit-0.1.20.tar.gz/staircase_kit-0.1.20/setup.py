# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['staircase',
 'staircase.commands',
 'staircase.commands.asana',
 'staircase.commands.config',
 'staircase.commands.envs',
 'staircase.commands.health',
 'staircase.commands.marketplace',
 'staircase.commands.postman',
 'staircase.commands.postman.import_',
 'staircase.lib',
 'staircase.lib.sdk',
 'staircase.lib.sdk.ci']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0.0,<4.0.0',
 'aiostream',
 'asana>=3.2.1,<4.0.0',
 'boto3',
 'click',
 'cryptography',
 'curlify',
 'mypy',
 'plumbum',
 'pydantic',
 'pyyaml',
 'requests>=2.28.2,<3.0.0',
 'rich',
 'uncurl']

entry_points = \
{'console_scripts': ['sc = staircase.cli:launch_cli',
                     'staircase = staircase.cli:launch_cli']}

setup_kwargs = {
    'name': 'staircase-kit',
    'version': '0.1.20',
    'description': '',
    'long_description': '**Table of contents**\n- [Note](#note)\n- [Features](#features)\n- [Installation](#installation)\n  - [Requirements](#requirements)\n    - [Git token](#git-token)\n    - [Hot get Postman API Key](#hot-get-postman-api-key)\n  - [Installing](#installing)\n  - [Configuring](#configuring)\n- [How to use](#how-to-use)\n\n# Note\n- All your data is stored inside `$HOME/.staircase` folder. Don`t share this!\n# Features\n- Postman management. You can import api`s and your environments into it.\n- CI flow management. You can easily run pipeline on any product, pick steps you only need and get output from it.\n\n# Installation\n## Requirements\n- [fzf](https://github.com/junegunn/fzf#installation)\n- [Git token](#git-token)\n- [Postman API Key](#hot-get-postman-api-key)\n- Marketplace API key\n\n### Git token\nUsed for clone product.\nGitHub token. Go to GitHub.com/Settings/Developer settings/Personal access token/New/Enable SSO.\nAdd checks to enable repo access.\n\n### Hot get Postman API Key\nFollow steps via app or website:\n- Click on profile pic \n- Settings \n- API keys \n- Generate API key\n  Consider verify that expiration date is okay, you are going need to renew it after.\n\n## Installing \n- Open terminal.\n- `pip install staircase-kit`\n\n## Configuring\n- Open terminal.\n- Run command `staircase config setup` or edit file `staircase config file-path`.\n\n# How to use\n- Open terminal\n- Run command `staircase` or `sc`\n- You can run `--help` to any command to get extra info.\n',
    'author': 'Zik',
    'author_email': 'zikunov.vladislav@staircase.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
