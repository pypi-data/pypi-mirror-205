# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kolena',
 'kolena._api',
 'kolena._api.v1',
 'kolena._utils',
 'kolena._utils.dataframes',
 'kolena.classification',
 'kolena.classification.multiclass',
 'kolena.detection',
 'kolena.detection._internal',
 'kolena.fr',
 'kolena.workflow',
 'kolena.workflow.metrics']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.1,<10.0.0',
 'Shapely>=1.8.5,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'dacite>=1.6',
 'deprecation>=2.1.0,<3.0.0',
 'numpy>=1.19',
 'pandas>=1.1,<1.6',
 'pandera>=0.9.0',
 'pyarrow>=8',
 'pydantic>=1.8',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.20',
 'retrying>=1.3.3,<2.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'tqdm>=4,<5']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata<5.0',
                             'typing-extensions>=4.5.0,<5.0.0']}

entry_points = \
{'console_scripts': ['kolena = kolena._utils.cli:run']}

setup_kwargs = {
    'name': 'kolena-client',
    'version': '0.65.0',
    'description': "Client for Kolena's machine learning (ML) testing and debugging platform.",
    'long_description': '<p align="center">\n  <img src="https://app.kolena.io/api/developer/docs/html/_static/wordmark-purple.svg" width="400" alt="Kolena" />\n</p>\n\n<p align=\'center\'>\n  <a href="https://pypi.python.org/pypi/kolena-client"><img src="https://img.shields.io/pypi/v/kolena-client" /></a>\n  <a href="https://www.apache.org/licenses/LICENSE-2.0"><img src="https://img.shields.io/pypi/l/kolena-client" /></a>\n  <a href="https://docs.kolena.io"><img src="https://img.shields.io/badge/docs-Tutorial%20%26%20Usage-6434c1" /></a>\n  <a href="https://app.kolena.io/api/developer/docs/html/index.html"><img src="https://img.shields.io/badge/docs-API%20Reference-6434c1" /></a>\n</p>\n\n---\n\n[Kolena](https://www.kolena.io) is a comprehensive machine learning testing and debugging platform to surface hidden\nmodel behaviors and take the mystery out of model development. Kolena helps you:\n\n- Perform high-resolution model evaluation\n- Understand and track behavioral improvements and regressions\n- Meaningfully communicate model capabilities\n- Automate model testing and deployment workflows\n\n`kolena-client` is the Python client library for programmatic interaction with Kolena.\n\n## Documentation\n\nVisit [docs.kolena.io](https://docs.kolena.io/) for tutorial and usage documentation and the\n[API Reference](https://app.kolena.io/api/developer/docs/html/index.html) for detailed `kolena-client` typing and\nfunction documentation.\n',
    'author': 'Kolena Engineering',
    'author_email': 'eng@kolena.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kolena.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
