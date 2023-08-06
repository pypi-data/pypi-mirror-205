# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['refurb_json_minify']

package_data = \
{'': ['*']}

install_requires = \
['refurb>=1.4']

entry_points = \
{'refurb.plugins': ['module = refurb_json_minify']}

setup_kwargs = {
    'name': 'refurb-json-minify',
    'version': '1.0.0',
    'description': 'Detects places where JSON output can be minified',
    'long_description': '# refurb-json-minify\n\nA small plugin for [Refurb](https://github.com/dosisod/refurb) aimed at minifying JSON outputs.\n\n## Why is this important?\n\nJSON is a widely used format for data exchange, whether that be APIs talking over the\ninternet, metadata being stored in a database, or config files stored on a user\'s\nfilesystem. Although CPU and harddrive space is getting cheaper and cheaper, it isn\'t\nfree, and being mindful of resources can lead to faster and more efficient programs.\n\n## Supported Checks\n\n### `JMIN100`: Use `separators`\n\nThe [`json.dump`](https://docs.python.org/3/library/json.html#json.dump) and\n[`json.dumps`](https://docs.python.org/3/library/json.html#json.dumps) functions\nallow for an optional `separators` field which specifies what characters to use\nfor colons (`:`) and commas (`,`) in the JSON output. Normally there is whitespace\nafter these characters, but you can change this to use a more compact format.\n\nHere is a simple example comparing the output of `json.dumps()` with and without\n`separators` specified:\n\n```python\nimport json\n\ndata = {\n  "hello": "world",\n  "numbers": [1, 2, 3, 4],\n}\n\na = json.dumps(data)\nb = json.dumps(data, separators=(",", ":"))\n\nprint(f"{len(a)=}", f"{len(b)=}")\n```\n\nWhen we run this, we get:\n\n```\nlen(a)=43 len(b)=37\n```\n\nBy reducing the whitespace in our JSON output we where able to shave off 6 bytes, or about\n16% in this example.\n\n### `JMIN101`: Don\'t `json.dump()` integers\n\nDon\'t call `json.dump()` on integers, use `str()` instead since they share the\nsame representation.\n',
    'author': 'dosisod',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dosisod/refurb-json-minify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
