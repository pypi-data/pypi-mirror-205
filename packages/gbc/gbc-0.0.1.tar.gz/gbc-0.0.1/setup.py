# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gbc']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['gbc = gbc.__main__:main']}

setup_kwargs = {
    'name': 'gbc',
    'version': '0.0.1',
    'description': 'A Python gopher client.',
    'long_description': '![gb logo, a gopher in a ball](https://src.tty.cat/supakeen/gb/raw/branch/master/doc/_static/logo-doc.png)\n\n# gbc\n',
    'author': 'Simon de Vlieger',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/supakeen/gbc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
