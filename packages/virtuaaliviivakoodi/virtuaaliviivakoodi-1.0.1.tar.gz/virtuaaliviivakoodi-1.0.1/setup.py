# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virtuaaliviivakoodi',
 'virtuaaliviivakoodi.constants',
 'virtuaaliviivakoodi.exceptions',
 'virtuaaliviivakoodi.normalizers',
 'virtuaaliviivakoodi.utils',
 'virtuaaliviivakoodi.validators']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'virtuaaliviivakoodi',
    'version': '1.0.1',
    'description': "Python library for generating Finnish virtuaaliviivakoodi's",
    'long_description': '# Finnish virtuaaliviivakoodi generation\n\n[![PyPI version](https://badge.fury.io/py/virtuaaliviivakoodi.svg)](https://badge.fury.io/py/virtuaaliviivakoodi)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\nVirtuaaliviivakoodi is a Python library for generating virtual barcodes based on Finanssiala\'s [pankkiviivakoodi spec](https://www.finanssiala.fi/wp-content/uploads/2021/03/Pankkiviivakoodi-opas.pdf).\n\n## Installation\n\n```bash\npip install virtuaaliviivakoodi\n```\n\n## Usage\n\n```python\nfrom virtuaaliviivakoodi import virtuaaliviivakoodi\n\nvirtuaaliviivakoodi(\n\tiban="FI49 5000 9420 0287 30",\n\treference="12345 67907",\n\tdue_date=date(2022, 12, 12),\n\teuro_amount=100.20,\n)\n\n# > "449500094200287300001002000000000000001234567907201212"\n\n```\n\n## Function arguments\n\n| Argument      | Type          | Description                                                                                                                                                                                                   |\n| ------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |\n| `iban`        | `str`         | Mandatory. Payment receiver\'s IBAN. Must be in Finnish format. E.g.: `"FI49 5000 9420 0287 30"` or `"FI4950009420028730"`                                                                                     |\n| `reference`   | `str` `int`   | Mandatory. Invoice reference in Finnish or international (RF) format. May invluce whitespace characters. E.g. `"12345 67907"`, `"1234567907"`, `1234567907` or `"RF92 1234 2345"`                             |\n| `due_date`    | `date`        | Mandatory. Invoice due date as a Python date object.                                                                                                                                                          |\n| `euro_amount` | `float` `int` | Mandatory. Invoice total amount in Euros. Must be positive number. According [the spec](https://www.finanssiala.fi/wp-content/uploads/2021/03/Pankkiviivakoodi-opas.pdf) amount must be smaller than 1000000. |\n\n## Exceptions\n\nExceptions can be imported the following way:\n\n```python\nfrom virtuaaliviivakoodi.exceptions import (\n\tVirtuaaliviivakoodiException,\n\tInvalidIBANException,\n\tInvalidReferenceException,\n\tInvalidEuroAmountException,\n\tInvalidDueDateException,\n)\n```\n\n| Exception                      | Description                                               |\n| ------------------------------ | --------------------------------------------------------- |\n| `VirtuaaliviivakoodiException` | Base exception class for all of the following exceptions. |\n| `InvalidIBANException`         | Raised for invalid IBANs                                  |\n| `InvalidReferenceException`    | Raised for invalid references                             |\n| `InvalidEuroAmountException`   | Raised for invalid euro amounts                           |\n| `InvalidDueDateException`      | Raised for invalid due dates                              |\n',
    'author': 'Juho Enala',
    'author_email': 'juho.enala@nocfo.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
