# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leap_model_rebuilder']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=3.19.6,<4.0.0', 'tensorflow-macos==2.12.0', 'tensorflow==2.12.0']

setup_kwargs = {
    'name': 'leap-model-rebuilder',
    'version': '0.1.6.dev1',
    'description': '',
    'long_description': '# leap-model-rebuilder\nKeras model rebuilder tool for model rebuilding with alterations\n',
    'author': 'dorhar',
    'author_email': 'doron.harnoy@tensorleap.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tensorleap/leap-model-rebuilder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
