# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chalice_spec']

package_data = \
{'': ['*']}

install_requires = \
['apispec>=6.0.2,<7.0.0']

setup_kwargs = {
    'name': 'chalice-spec',
    'version': '0.6.0',
    'description': 'Chalice x APISpec x Pydantic plug-ins',
    'long_description': '# chalice-spec\n\n[![Python package](https://github.com/TestBoxLab/chalice-spec/actions/workflows/test.yml/badge.svg)](https://github.com/TestBoxLab/chalice-spec/actions/workflows/test.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Chalice × APISpec × Pydantic plug-ins**\n\nCombines the power of Chalice, APISpec, and Pydantic to make AWS Chalice apps easily documented\n\n## Installation\n\nFirst, add chalice-spec:\n\n```shell\npoetry add chalice_spec\n```\n\nWe consider Chalice, APISpec, and Pydantic "peer dependencies." We only include them as dev\ndependencies in our codebase, and you may need to install them in yours if you haven\'t\nalready.\n\n```shell\npoetry add chalice apispec pydantic\n```\n\n## Setup\n\nchalice-spec provides a subclass of the main `Chalice` class, called `ChaliceWithSpec`.\nHere is an example of how to get started:\n\nBefore:\n\n```python\nfrom chalice import Chalice\n\napp = Chalice(app_name="hello_world")\n```\n\nAfter:\n\n```python\nfrom chalice_spec import ChaliceWithSpec, PydanticPlugin\nfrom apispec import APISpec\n\nspec = APISpec(...,\n               plugins=[PydanticPlugin()])\n\napp = ChaliceWithSpec(app_name="hello_world", spec=spec)\n```\n\nIf you use\n\n```python\nChaliceWithSpec(..., generate_default_docs=True)\n```\n\nthe plugin will generate empty docs (with empty request and response schemas) for every endpoint that you\'ve defined in your app. This can be useful as a starting point / overview while developing.\n\n## Usage\n\nTo document your API, use your existing Pydantic models and add kwargs to Chalice decorators.\n\n**Before:**\n```python\n@app.route(\'/\', methods=["POST"])\ndef example():\n    body = MySchema.parse_obj(app.current_request.json_body)\n```\n\n**After:**\n```python\n@app.route(\'/\', methods=["POST"], docs=Docs(\n    post=Operation(request=MySchema)\n))\ndef example():\n    body = MySchema.parse_obj(app.current_request.json_body)\n```\n\nIf you have multiple methods supported, you may have something like:\n\n```python\n@app.route(\'/\', methods=["POST", "PUT"],\n           docs=Docs(\n               post=Operation(request=MyCreateSchema, response=MyReadSchema),\n               put=Operation(request=MyEditSchema, response=MyReadSchema)\n           )\ndef example():\n    # code goes here\n    pass\n```\n\n## Auto-Generation\n\n### Default Empty Docs\n\nIf you use:\n```python\nChalicePlugin(generate_default_docs=True)\n```\nthe plugin will generate empty docs (with empty request and response schemas) for every endpoint that you\'ve defined in your app. This can be useful as a starting point / overview while developing.\n\n### Path Parameters\n\nThese are inferred from the path itself. Any identifiers inside curly braces in a path is added as a string path parameter for that path. e.g. for the path `/users/{id}/friends/{f_id}`, the path parameters `id` and `f_id` will be added to the spec.\n\nTo disable this behaviour, define your own parameters or set them to an empty list:\n\n```python\nOperation(request=MySchema, response=MyOtherSchema, parameters=[])\n```\n\n### Tags\n\nTags are used in things like Swagger to group endpoints into logical sets. If you don\'t supply any tags, chalice-spec will add a tag for each endpoint that is the first segment of the path. e.g. `/users`, `/users/{id}/friends`, and `/users/{id}/posts` will all be tagged with `users`.\n\nTo disable this behaviour, define `tags` in your operation (either with the tags you want, or an empty list):\n\n```python\nOperation(request=MySchema, response=MyOtherSchema, tags=[])\n```\n\n### Summary and Description\n\nEndpoint summaries and descriptions are inferred from the route docstring. The first line of the docstring is used as the summary, and all other lines become the description:\n\n```python\n@app.route(\'/users/{id}\', methods=[\'GET\'], docs=Docs(response=UserSchema))\ndef get_user(id):\n    """\n    Retrieve a user object.\n    User\'s can\'t retrieve other users using this endpoint - only themselves.\n    """\n```\n\nTo disable this behaviour, you can define your own summary/description or set them to empty strings:\n\n```python\nOperation(request=MySchema, response=MyOtherSchema, summary=\'\', description=\'\')\n```\n\n\n### API\n\n- [ ] TODO: this section coming soon!\n',
    'author': 'Jake Wood',
    'author_email': 'jake@testbox.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TestBoxLab/chalice-spec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
