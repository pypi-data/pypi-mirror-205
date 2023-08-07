# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aspreno']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx>=6.1.3,<7.0.0',
          'insegel>=1.3.1,<2.0.0',
          'sphinxcontrib-fulltoc>=1.2.0,<2.0.0']}

setup_kwargs = {
    'name': 'aspreno',
    'version': '1.0.0.dev1',
    'description': '',
    'long_description': '# Aspreno\n\n<div align="center">\n    <!-- License -->\n    <a href="https://github.com/Predeactor/Aspreno/blob/main/README.md">\n        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/aspreno">\n    </a>\n    <!-- Version -->\n    <a href="https://pypi.org/project/aspreno">\n        <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/aspreno">\n    </a>\n    <!-- Supported Python version -->\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/aspreno">\n    <!-- Codecov -->\n    <a href="https://codecov.io/github/Predeactor/Aspreno" >\n        <img alt="Codecov report" src="https://codecov.io/github/Predeactor/Aspreno/branch/main/graph/badge.svg?token=YTLWE8VQYM"/>\n    </a>\n</div>\n\nPython 3 global error handling & self-handling exceptions.\n\n## Features\n\n- Global exception handling\n- Self-handleable exceptions\n- Able to report specific exceptions\n',
    'author': 'Predeactor',
    'author_email': 'pro.julien.mauroy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
