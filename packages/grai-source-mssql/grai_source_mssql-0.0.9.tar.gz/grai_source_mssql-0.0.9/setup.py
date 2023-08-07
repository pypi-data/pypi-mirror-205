# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grai_source_mssql']

package_data = \
{'': ['*']}

install_requires = \
['grai-client>=0.2.0,<0.3.0',
 'grai-schemas>=0.1.8,<0.2.0',
 'multimethod>=1.8,<2.0',
 'pydantic>=1.9.1,<2.0.0',
 'pyodbc>=4.0.35,<5.0.0']

setup_kwargs = {
    'name': 'grai-source-mssql',
    'version': '0.0.9',
    'description': '',
    'long_description': '# Grai SQL Server Integration\n\nThe SQL Server integration synchronizes metadata from your SQL Server database into your Grai data lineage graph.\n',
    'author': 'Ian Eaves',
    'author_email': 'ian@grai.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.grai.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
