# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grai_source_bigquery']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=3.5.0,<4.0.0',
 'grai-client>=0.2.0,<0.3.0',
 'grai-schemas>=0.1.9,<0.2.0',
 'multimethod>=1.8,<2.0',
 'pydantic>=1.9.1,<2.0.0',
 'setuptools>=67.1.0,<68.0.0']

setup_kwargs = {
    'name': 'grai-source-bigquery',
    'version': '0.0.5',
    'description': '',
    'long_description': '# Grai BigQuery Integration\n\nThe BigQuery integration synchronizes metadata from a BigQuery datawarehouse into your Grai data lineage graph.\n',
    'author': 'Edward Louth',
    'author_email': 'edward@grai.io',
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
