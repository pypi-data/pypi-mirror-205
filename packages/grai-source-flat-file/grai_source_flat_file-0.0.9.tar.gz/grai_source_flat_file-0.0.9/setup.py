# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grai_source_flat_file']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'grai-client>=0.2.0,<0.3.0',
 'grai-schemas>=0.1.10,<0.2.0',
 'multimethod>=1.8,<2.0',
 'pandas>=1.4.4,<2.0.0',
 'pydantic>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'grai-source-flat-file',
    'version': '0.0.9',
    'description': '',
    'long_description': '# Grai Flat File Integration\n\nThe Flat File integration synchronizes metadata from flat files including csv, feather, and parquet into your Grai data lineage graph.\n',
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
