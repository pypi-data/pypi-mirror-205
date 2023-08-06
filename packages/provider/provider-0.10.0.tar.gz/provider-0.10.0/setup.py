# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['provider',
 'provider.cli',
 'provider.config',
 'provider.config.tests',
 'provider.runtime',
 'provider.runtime.tests',
 'provider.runtime.tests.commonfate_provider_dist',
 'provider.runtime.tests.provider_example']

package_data = \
{'': ['*'], 'provider.runtime.tests': ['__snapshots__/aws_lambda_test/*']}

install_requires = \
['boto3>=1.26.82,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'common-fate-schema>=0.7.0,<0.8.0',
 'pydantic>=1.10.5,<2.0.0',
 'toml==0.10.2',
 'typing-extensions>=4.5.0,<5.0.0']

entry_points = \
{'console_scripts': ['provider = provider.cli.main:cli']}

setup_kwargs = {
    'name': 'provider',
    'version': '0.10.0',
    'description': 'Common Fate Provider Development Kit',
    'long_description': '# Provider Development Kit\n\nCommon Fate Provider Development Kit for Python.\n\n## What is a provider?\n\nA Provider is a Python service which provides a consistent API for managing fine-grain permissions.\n\nManaging permissions in cloud providers, SaaS applications, and CI/CD platforms usually requires access to highly sensitive secrets, like administrative API tokens. The Provider framework allows for access to be granted and revoked to these platforms without requiring direct access to these tokens:\n\n![diagram of Provider framework](./docs/provider.drawio.svg)\n\n## What does the Provider Development Kit do?\n\nThe Provider Development Kit (PDK) makes it easy to develop and deploy Providers.\n\n```python\nclass Provider(provider.Provider):\n    api_url = provider.String()\n\n@access.target()\nclass Target:\n    ...\n\n@access.grant()\ndef grant(p: Provider, subject: str, target: Target):\n    # perform API calls here to grant access\n    ...\n\n@access.revoke()\ndef revoke(p: Provider, subject: str, target: Target):\n    # perform API calls here to revoke access\n    ...\n```\n\nThe PDK handles configuration and packaging into a cloud-native function which can be executed by an application.\n\n## Supported runtimes\n\nCurrently the supported runtimes for Providers are as follows:\n\n- AWS Lambda\n\n## Provider Schemas\n\nEach Provider has a strongly-typed schema. An example schema is shown below:\n\n```json\n{\n  "audit": {\n    "resourceLoaders": {},\n    "resources": {}\n  },\n  "config": {},\n  "target": {\n    "MyTarget": {\n      "schema": {\n        "first": {\n          "description": "first var",\n          "id": "first",\n          "resourceName": null,\n          "title": "First",\n          "type": "string"\n        }\n      }\n    }\n  }\n}\n```\n\nThe schema is based on [JSON Schema](https://json-schema.org/) and allows applications using Providers to interpret the available resources and display the appropriate UI.\n',
    'author': 'Common Fate',
    'author_email': 'hello@commonfate.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
