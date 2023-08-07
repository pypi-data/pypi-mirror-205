# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grai_schemas', 'grai_schemas.v1', 'grai_schemas.v1.metadata']

package_data = \
{'': ['*']}

install_requires = \
['multimethod>=1.9.1,<2.0.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'grai-schemas',
    'version': '0.1.12',
    'description': '',
    'long_description': '# Grai Schemas\n\nGrai Schemas provide reference implementations in Python for objects used in Grai.\nSo long as your data follows a schema implementation provided in this repository it will be able to interoperate with\nall of the other Grai services including the server REST API, yaml serialization, and data integrations.\n',
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
