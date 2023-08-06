# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hgchat']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.29.0,<3.0.0']

setup_kwargs = {
    'name': 'hgchat',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Hugging Chat Python\n\n## Installation\n\n### As library\n\n### As an interactive prompt\n\n```\ngit clone https://github.com/Bavarder/hgchat.git\ncd hgchat\n```\n\n## Usage\n\n### As library\n\n### As an interactive prompt\n\n``` shell\npython chat.py\n```\n\n',
    'author': '0xMRTT',
    'author_email': '0xMRTT@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
