# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_mod_auth_gssapi']

package_data = \
{'': ['*']}

install_requires = \
['flask<3.0.0', 'gssapi>=1.6.2,<2.0.0']

setup_kwargs = {
    'name': 'flask-mod-auth-gssapi',
    'version': '0.3.0',
    'description': "A Flask extention to make use of the authentication provided by the mod_auth_gssapi extention of Apache's HTTPd.",
    'long_description': "# Flask Mod Auth GSSAPI\n\n\nA Flask extention to make use of the authentication provided by the\n[mod_auth_gssapi](https://github.com/gssapi/mod_auth_gssapi) extention of\nApache's HTTPd. See [FASJSON](https://github.com/fedora-infra/fasjson) for a\nusage example.\n",
    'author': 'Fedora Infrastructure',
    'author_email': 'admin@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedora-infra/flask-mod-auth-gssapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
