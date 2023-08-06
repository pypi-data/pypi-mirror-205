# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['switchbladecli', 'switchbladecli.cli', 'switchbladecli.modes']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.58.1,<2.0.0',
 'checksumdir>=1.2.0,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'tomlkit>=0.11.7,<0.12.0']

entry_points = \
{'console_scripts': ['swb = switchbladecli.cli.__main__:switchbladecli']}

setup_kwargs = {
    'name': 'sentient-switchblade',
    'version': '0.1.0',
    'description': 'Unleash Dev Tool Mastery with a Flick of Your Wrist',
    'long_description': 'None',
    'author': 'JensRoland',
    'author_email': 'mail@jensroland.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kegstand.dev/sentient-switchblade',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
