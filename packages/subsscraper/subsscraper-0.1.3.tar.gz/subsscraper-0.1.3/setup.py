# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.conf']

package_data = \
{'': ['*']}

install_requires = \
['hydra-core>=1.3.2,<2.0.0',
 'loguru>=0.7.0,<0.8.0',
 'requests>=2.28.2,<3.0.0',
 'yt-dlp>=2023.3.4,<2024.0.0']

entry_points = \
{'console_scripts': ['search = src.search:main',
                     'subscrape = src.subscraper:main']}

setup_kwargs = {
    'name': 'subsscraper',
    'version': '0.1.3',
    'description': '',
    'long_description': 'SubScraper\n---------\n\nRun command for generate urls\n```commandline\nsearch\nsearch search.cnt=2 # for 2 urls\nsearch \'search.query="лекции таймкоды"\' search.cnt=2 # override cyrillic (more quotes)\n```\n\nRun command for subscrape urls\n```commandline\nsubscrape\n```\n\nDefault configs\n```commandline\nsearch:\n  output_folder: data\n  result_file: urls.txt\n  cnt: 10\n  query: машинное обучение лекции таймкоды\n\nscraper:\n  output_folder: ${search.output_folder}/dataset\n```\n\n',
    'author': 'tupiznak',
    'author_email': 'akej-vonavi@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
