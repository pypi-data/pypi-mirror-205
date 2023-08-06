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
    'version': '0.0.3',
    'description': 'Spec protocol tests for lightning network implementations',
    'long_description': '<div align="center">\n  <h1>lnprototest</h1>\n\n  <p>\n    <strong>a Testsuite for the Lightning Network Protocol</strong>\n  </p>\n\n  <h4>\n    <a href="https://github.com/rustyrussell/lnprototest">Project Homepage</a>\n  </h4>\n \n  <a href="https://github.com/rustyrussell/lnprototest/actions">\n    <img alt="GitHub Workflow Status (branch)" src="https://img.shields.io/github/workflow/status/rustyrussell/lnprototest/Integration%20testing/master?style=flat-square"/>\n  </a>\n  \n  <a href="https://github.com/vincenzopalazzo/lnprototest/blob/vincenzopalazzo/styles/HACKING.md">\n    <img src="https://img.shields.io/badge/doc-hacking-orange?style=flat-square" />\n  </a>\n\n</div>\n\nlnprototest is a set of test helpers written in Python3, designed to\nmake it easy to write new tests when you propose changes to the\nlightning network protocol, as well as test existing implementations.\n\n## Install requirements\n\nTo install the necessary dependences\n\n```bash\npip3 install poetry\npoetry shell\npoetry install\n```\n\nWell, now we can run the test\n\n## Running test\n\nThe simplest way to run is with the "dummy" runner:\n\n\tmake check\n\nHere are some other useful pytest options:\n\n1. `-n8` to run 8-way parallel.\n2. `-x` to stop on the first failure.\n3. `--pdb` to enter the debugger on first failure.\n4. `--trace` to enter the debugger on every test.\n5. `-k foo` to only run tests with \'foo\' in their name.\n6. `tests/test_bolt1-01-init.py` to only run tests in that file.\n7. `tests/test_bolt1-01-init.py::test_init` to only run that test.\n8. `--log-cli-level={LEVEL_NAME}` to enable the logging during the test execution.\n\n### Running Against A Real Node.\n\nThe more useful way to run is to use an existing implementation. So\nfar, core-lightning is supported.  You will need:\n\n1. `bitcoind` installed, and in your path.\n2. [`lightningd`](https://github.com/ElementsProject/lightning/) compiled with\n   `--enable-developer`. By default the source directory should be\n   `../lightning` relative to this directory, otherwise use\n   `export LIGHTNING_SRC=dirname`.\n3. Install any python requirements by\n   `pip3 install -r lnprototest/clightning/requirements.txt`.\n\nThen you can run\n\n\tmake check PYTEST_ARGS=\'--runner=lnprototest.clightning.Runner\'\n\nor directly:\n\n    pytest --runner=lnprototest.clightning.Runner\n\n# Further Work\n\nIf you want to write new tests or new backends, see [HACKING.md](HACKING.md).\n\nLet\'s keep the sats flowing!\n\nRusty.\n',
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
