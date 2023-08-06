# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lnprototest',
 'lnprototest.backend',
 'lnprototest.clightning',
 'lnprototest.stash',
 'lnprototest.utils']

package_data = \
{'': ['*']}

install_requires = \
['crc32c>=2.2.post0,<3.0',
 'pyln-bolt1>=1.0.222,<2.0.0',
 'pyln-bolt2>=1.0.222,<2.0.0',
 'pyln-bolt4>=1.0.222,<2.0.0',
 'pyln-bolt7>=1.0.246,<2.0.0',
 'pyln-client>=0.12.0,<0.13.0',
 'pyln-proto>=0.12.0,<0.13.0',
 'pyln-testing>=0.12.0,<0.13.0',
 'python-bitcoinlib>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'lnprototest',
    'version': '0.0.2',
    'description': 'Spec protocol tests for lightning network implementations',
    'long_description': 'None',
    'author': 'Rusty Russell',
    'author_email': 'rusty@blockstream.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
