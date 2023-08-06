# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacs']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0', 'pydantic>=1.10.7,<2.0.0']

setup_kwargs = {
    'name': 'spacs',
    'version': '0.0.1',
    'description': 'Simple Pydantic AIOHTTP Client Sessions',
    'long_description': '# SPACS: Simple Pydantic AIOHTTP Client Sessions\n\nA package to assist in managing and using long-lived AIOHTTP client sessions with simplicity. Built to handle Pydantic objects.\n\n## Features\n\n* Handles request params and bodies as either Pydantic objects or native Python dictionaries, converting items to JSON-safe format.\n* Abstracts away internals of managing the request/response objects, instead either returning parsed response content on success, or raising a specialized error object.\n* Automatically manages persistent connections to be shared over extended lifespan across application, cleaning up all open connections on teardown.\n* Utilizes modern Python type hinting.\n\n## Usage\n\n```python\nimport spacs\nfrom pydantic import BaseModel\n\n...\n\nexample_client = spacs.SpacsClient(base_url="http://example.com")\n\n# Basic request with error handling\ntry:\n    apple_response = await example_client.get("fruit/apple", params={"cultivar": "honeycrisp"})\nexcept spacs.SpacsRequestError as error:\n    print({"code": error.status_code, "reason": error.reason})\n\n# Sending Pydantic objects via HTTP POST\nclass MyModel(BaseModel):\n    name: str\n    age: int\n\nexample_object = MyModel(name="James", age=25)\nperson_response = await example_client.post("person", body=example_object)\n\n# Manually closing a session\nawait example_client.close()\n# Alternatively, to close all open sessions:\nawait spacs.SpacsClient.close_all()\n```\n\n## Building\n\n```\npoetry build\n```\n',
    'author': 'rlebel12',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
