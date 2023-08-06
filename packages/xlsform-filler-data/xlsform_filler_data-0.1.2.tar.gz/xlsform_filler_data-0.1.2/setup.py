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
{'console_scripts': ['xlsform-filler-data = '
                     'xlsform_filler_data.xlsform_filler_data:cli']}

setup_kwargs = {
    'name': 'xlsform-filler-data',
    'version': '0.1.2',
    'description': 'A tool for generating fake testing data based on an XLSform. ',
    'long_description': "# XLSform filler data\n\nA commandline tool for creating dummy/test data from XLSform surveys.\n\n## Installation\n```pip install xlsform-filler-data```\n\n## Usage\nTo create a dummy dataset, with a default number of rows(100) from a XLSform source:\n```xlsform-filler-data <source-file-path>/<filename.xlsx>```\n\nTo specify the number of rows to create, use the *-r* flag. Example:\n```xlsform-filler-data <source-file-path>/<filename.xlsx> -r 200```\n\nTo specify the output path and filename, pass the *-o* flag. Example:\n```xlsform-filler-data <source-file-path>/<filename.xlsx> -o <./myfile.xlsx>```\n\n## Roadmap\nAs of version *0.1.1* the tool does not properly randomise multiple choice questions; omits some variables such as 'start' and 'end'; does not maintain the order of the variables; and does not incorporate constraints or cascading choice lists. These limitations will be adddressed in future releases.",
    'author': 'Brian Mc Donald',
    'author_email': 'brian@brianmcdonald.me',
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
