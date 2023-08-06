# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*'], 'src': ['conf/*']}

install_requires = \
['hydra-core>=1.3.2,<2.0.0',
 'loguru>=0.7.0,<0.8.0',
 'requests>=2.28.2,<3.0.0',
 'yt-dlp>=2023.3.4,<2024.0.0']

setup_kwargs = {
    'name': 'subsscraper',
    'version': '0.1.0',
    'description': '',
    'long_description': 'SubScraper\n---------\n```commandline\ncheck\n```\n\n',
    'author': 'tupiznak',
    'author_email': 'akej-vonavi@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
