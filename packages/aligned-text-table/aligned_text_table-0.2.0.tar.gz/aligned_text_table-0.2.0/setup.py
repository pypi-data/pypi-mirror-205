# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aligned_text_table']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aligned-text-table',
    'version': '0.2.0',
    'description': 'Parser for space-aligned tables in plain text',
    'long_description': '# Aligned text table\n\nA parser for tables in plain text that are aligned with spaces, e.g.:\n\n```\nThis is     Column two   This one\ncolumn one               is column\n                         three\n```\n\n## Usage\n\n```\n>>> from aligned_text_table import parse_row\n\n>>> parse_row(\n...     lines=[\n...         "This is     Column two   This one ",\n...         "column one               is column",\n...         "three    "\n...     ],\n...     keys=["one", "two", "three"]\n... )\n\n{\n    "one": "This is column one",\n    "two": "Column two",\n    "three": "This one is column three"\n}\n```\n\n## Tests\n\nTo run tests, install and run Tox:\n\n```\npip3 install tox\ntox\n```\n',
    'author': 'Robin Winslow',
    'author_email': 'robin@robinwinslow.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nottrobin/aligned-text-table',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
