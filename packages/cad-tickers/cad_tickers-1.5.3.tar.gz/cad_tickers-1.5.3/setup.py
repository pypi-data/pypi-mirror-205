# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cad_tickers',
 'cad_tickers.exchanges',
 'cad_tickers.exchanges.tsx',
 'cad_tickers.news',
 'cad_tickers.news.ceo',
 'cad_tickers.sedar',
 'cad_tickers.util']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'coverage>=5.2,<6.0',
 'lxml>=4.5.2,<5.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.3.0,<2.0.0',
 'random-user-agent>=1.0.1,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'xlrd>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'cad-tickers',
    'version': '1.5.3',
    'description': 'Various Stock Utilties Created by me',
    'long_description': '[![PyPI version](https://badge.fury.io/py/cad-tickers.svg)](https://badge.fury.io/py/cad-tickers) [![Downloads](https://pepy.tech/badge/cad-tickers)](https://pepy.tech/project/cad-tickers) [![Documentation Status](https://readthedocs.org/projects/cad-tickers/badge/?version=latest)](https://cad-tickers.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/FriendlyUser/cad_tickers/branch/master/graph/badge.svg)](https://codecov.io/gh/FriendlyUser/cad_tickers)\n \n## Cad Tickers\nFunction to extract exchange data from the cse and tsx websites and various other data sources. This package is primarily focussed on scrapping data for the canadian stock market.\n\n\nThe entire 0.2.x version of tsx functions are now depricated.\n\nTsx has switched to graphql which I like.\n\n\n### How to run tests\n\n```\npytest\n```\n\n```\n# Needed for readthedocs documentation\npoetry export -f requirements.txt > requirements.txt.\n```\n\nOr checkout some of my books [![Python Programming](https://m.media-amazon.com/images/I/41Mj384vgeL._SY346_.jpg)](https://www.amazon.com/dp/B0BXFLYRBD)\n\n\n#### Donate\n\nIf you would like to motivate me to spend more time improving open source projects please consider donating.\n\n[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Z6M6Y83D3URSU&item_name=Motivating+me+to+continue+to+produce+open+source+projects&currency_code=CAD)\n',
    'author': 'David Li',
    'author_email': 'davidli012345@gmail.com',
    'maintainer': 'David Li',
    'maintainer_email': 'davidli012345@gmail.com',
    'url': 'https://github.com/FriendlyUser/cad_tickers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
