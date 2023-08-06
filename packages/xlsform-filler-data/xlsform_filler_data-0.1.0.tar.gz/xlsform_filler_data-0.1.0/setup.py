# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlsform_filler_data']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'lorem-text>=2.1,<3.0',
 'openpyxl>=3.1.2,<4.0.0',
 'pandas>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['xlsform_filler_data = '
                     'xlsform_filler_data.xlsform_filler_data:cli']}

setup_kwargs = {
    'name': 'xlsform-filler-data',
    'version': '0.1.0',
    'description': 'A tool for generating fake testing data based on an XLSform. ',
    'long_description': '',
    'author': 'Brian Mc Donald',
    'author_email': 'brian@brianmcdonald.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
