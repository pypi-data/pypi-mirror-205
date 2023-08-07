# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grai_cli',
 'grai_cli.api',
 'grai_cli.api.config',
 'grai_cli.api.server',
 'grai_cli.api.telemetry',
 'grai_cli.settings',
 'grai_cli.utilities']

package_data = \
{'': ['*']}

install_requires = \
['confuse>=2.0.0,<3.0.0',
 'grai-client>=0.2.4,<0.3.0',
 'grai-schemas>=0.1.5,<0.2.0',
 'multimethod>=1.9,<2.0',
 'posthog>=2.2.0,<3.0.0',
 'pydantic-yaml>=0.11.1,<0.12.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['grai = grai_cli.api.entrypoint:app']}

setup_kwargs = {
    'name': 'grai-cli',
    'version': '0.1.10',
    'description': '',
    'long_description': "# Grai CLI\n\nThe `grai-cli` package is a commandline library for interacting with your Grai data lineage.\nIt brings the full power of data lineage to your command line, allowing you to directly query the database wherever you're working.\n",
    'author': 'Ian Eaves',
    'author_email': 'ian@grai.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.grai.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
