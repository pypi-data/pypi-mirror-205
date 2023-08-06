# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['gpc',
 'gpc.executors',
 'gpc.helpers',
 'gpc.helpers.tests',
 'gpc.schema',
 'gpc.templates',
 'gpc.templates.mail',
 'gpc.templates.tests',
 'gpc.tests']

package_data = \
{'': ['*'],
 'gpc.tests': ['vectors/*',
               'vectors/layered_includes/lvl1/*',
               'vectors/layered_includes/lvl1/lvl2/*']}

install_requires = \
['anyconfig',
 'arrow>=1.0',
 'attrs',
 'boltons',
 'click-config-file',
 'click>=7',
 'colorama',
 'dictns',
 'dotmap',
 'fastjsonschema',
 'gitchangelog>=3.0.4,<4.0.0',
 'gitpython',
 'importlib-resources',
 'jinja2>=2.1',
 'jsonschema',
 'path',
 'python-gitlab<3',
 'pyyaml',
 'rfc3987',
 'ruamel.yaml',
 'seep',
 'sentry-sdk',
 'sortedcontainers',
 'strict-rfc3339',
 'structlog',
 'webcolors']

entry_points = \
{'console_scripts': ['gpc = gpc.cli:main']}

setup_kwargs = {
    'name': 'gitlab-project-configurator',
    'version': '0.0.0',
    'description': 'Manage, deploy and update your gitlab projects configuration as source.',
    'long_description': 'None',
    'author': 'nestor',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
