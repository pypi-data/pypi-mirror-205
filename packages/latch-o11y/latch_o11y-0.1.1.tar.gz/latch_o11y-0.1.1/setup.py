# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latch_o11y']

package_data = \
{'': ['*']}

install_requires = \
['latch-config>=0.1.1,<0.2.0',
 'opentelemetry-api>=1.15.0,<2.0.0',
 'opentelemetry-exporter-otlp-proto-grpc>=1.15.0,<2.0.0',
 'opentelemetry-sdk>=1.15.0,<2.0.0',
 'orjson>=3.8.5,<4.0.0',
 'structlog>=22.3.0,<23.0.0']

setup_kwargs = {
    'name': 'latch-o11y',
    'version': '0.1.1',
    'description': 'Observability for latch python backend services',
    'long_description': '# python-o11y\n',
    'author': 'Max Smolin',
    'author_email': 'max@latch.bio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
