# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gbs']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0', 'python-magic>=0.4.27,<0.5.0', 'tornado>=6.0,<7.0']

entry_points = \
{'console_scripts': ['gbs = gbs.__main__:main']}

setup_kwargs = {
    'name': 'gbs',
    'version': '0.0.1',
    'description': 'A Python gopher server.',
    'long_description': '![gb logo, a gopher in a ball](https://src.tty.cat/supakeen/gb/raw/branch/master/doc/_static/logo-doc.png)\n\n# gbs\n',
    'author': 'Simon de Vlieger',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/supakeen/gbs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
