# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testvault']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'structlog>=23.1.0,<24.0.0']

setup_kwargs = {
    'name': 'testvault',
    'version': '0.1.0',
    'description': '',
    'long_description': '# testvault-python-sdk\n\nA Python SDK for TestVault. TestVault is a sample service used to demonstrate building Common Fate Access Providers to automate entitlements. TestVault is a fictional password management service similar to 1Password or Lastpass.\n\nCommon Fate hosts the TestVault service at `https://prod.testvault.granted.run`.\n\nThe source code for the TestVault service can be found at https://github.com/common-fate/testvault.\n',
    'author': 'Common Fate',
    'author_email': 'hello@commonfate.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
