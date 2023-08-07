# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fbench']

package_data = \
{'': ['*']}

install_requires = \
['bumbag>=5.0.0,<6.0.0', 'matplotlib>=3.7.1,<4.0.0', 'numpy>=1.24.2,<2.0.0']

setup_kwargs = {
    'name': 'fbench',
    'version': '0.3.0',
    'description': 'A collection of benchmark functions.',
    'long_description': '<h1 align="center">fBench</h1>\n\n<p align="center">\n<a href="https://pypi.org/project/fbench"><img alt="pypi" src="https://img.shields.io/pypi/v/fbench"></a>\n<a href="https://readthedocs.org/projects/fbench/?badge=latest"><img alt="docs" src="https://readthedocs.org/projects/fbench/badge/?version=latest"></a>\n<a href="https://github.com/estripling/fbench/actions/workflows/ci.yml"><img alt="ci status" src="https://github.com/estripling/fbench/actions/workflows/ci.yml/badge.svg?branch=main"></a>\n<a href="https://codecov.io/gh/estripling/fbench"><img alt="coverage" src="https://codecov.io/github/estripling/fbench/coverage.svg?branch=main"></a>\n<a href="https://github.com/estripling/fbench/blob/main/LICENSE"><img alt="license" src="https://img.shields.io/pypi/l/fbench"></a>\n</p>\n\n## About\n\nA collection of benchmark functions:\n\n- [Documentation](https://fbench.readthedocs.io/en/stable/index.html)\n- [Overview of fBench functions](https://fbench.readthedocs.io/en/stable/fBench-functions.html)\n- [API Reference](https://fbench.readthedocs.io/en/stable/autoapi/fbench/index.html)\n\n## Installation\n\n`fbench` is available on [PyPI](https://pypi.org/project/fbench/) for Python 3.8+:\n\n```console\npip install fbench\n```\n\n## Examples\n\nThe [`ackley`](https://fbench.readthedocs.io/en/stable/autoapi/fbench/index.html#fbench.ackley) function:\n\n```python\n>>> import fbench\n>>> round(fbench.ackley([1, 1]), 4)\n3.6254\n```\n\n## Contributing to fBench\n\nYour contribution is greatly appreciated!\nSee the following links to help you get started:\n\n- [Contributing Guide](https://fbench.readthedocs.io/en/latest/contributing.html)\n- [Developer Guide](https://fbench.readthedocs.io/en/latest/developers.html)\n- [Contributor Code of Conduct](https://fbench.readthedocs.io/en/latest/conduct.html)\n\n## License\n\n`fbench` was created by fBench Developers.\nIt is licensed under the terms of the BSD 3-Clause license.\n',
    'author': 'fBench Developers',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/estripling/fbench',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
