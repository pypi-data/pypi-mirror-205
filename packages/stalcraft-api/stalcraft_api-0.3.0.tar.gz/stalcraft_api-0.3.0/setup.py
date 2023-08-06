# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stalcraft']

package_data = \
{'': ['*'], 'stalcraft': ['data/global/*', 'data/ru/*']}

install_requires = \
['pydantic>=1.10.7,<2.0.0', 'pytz>=2021.1,<2022.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'stalcraft-api',
    'version': '0.3.0',
    'description': 'stalcraft api unofficial python library',
    'long_description': '<h1 align="center">stalcraft-api unofficial python library</h1>\n\n<p align="center">\n    <a href="https://pypi.org/project/stalcraft-api" alt="PyPi Package Version">\n        <img src="https://img.shields.io/pypi/v/stalcraft-api.svg?style=flat-square"/></a>\n    <a href="https://pypi.org/project/stalcraft-api" alt="Supported python versions">\n        <img src="https://img.shields.io/pypi/pyversions/stalcraft-api.svg?style=flat-square"/></a>\n    <a href="https://opensource.org/licenses/MIT" alt="MIT License">\n        <img src="https://img.shields.io/pypi/l/aiogram.svg?style=flat-squar"/></a>\n</p>\n\n\n<br>\n\n<p align="center">\n    <b>Official API documentation:</b> https://eapi.stalcraft.net\n</p>\n<p align="center">\n    <b>Before you can use the API, you must register your application and receive approval<b>\n</p>\n<p align="center">\n    <b>For testing Demo API is available<b>\n</p>\n<p align="center">\n    <a href="https://eapi.stalcraft.net/registration.html">more about applications</a>\n</p>\n\n\n<br>\n\n# 🔧 Install\n\n### Pip\n\n```console\npip install stalcraft-api --upgrade\n```\n\n<details>\n<summary>Manual</summary>\n\n```console\ngit clone git@github.com:onejeuu/stalcraft-api.git\n```\n\n```console\ncd stalcraft-api\n```\n\n```console\npip install -r requirements.txt\n```\n</details>\n\n\n<br>\n<br>\n\n# ⚡ Quick Start\n\n```python\nfrom stalcraft import AppClient\n\nTOKEN = "YOUR_TOKEN"\n\nclient = AppClient(token=TOKEN)\n```\n\n<br>\n<br>\n\n# 🚫 Exceptions\n\n```\nException\n├── InvalidToken\n├── StalcraftApiException\n│   ├── Unauthorised\n│   ├── InvalidParameter\n│   ├── NotFound\n│   └── RateLimitException\n└── ItemException\n    ├── ListingJsonNotFound\n    └── ItemIdNotFound\n```\n\n<br>\n<br>\n\n# 🔑 Tokens\n\n```python\nfrom stalcraft import Authorization\n\nCLIENT_ID = "YOUR_CLIENT_ID"\nCLIENT_SECRET = "YOUR_CLIENT_SECRET"\n\nauth = Authorization(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)\n```\n\n<details>\n<summary>Get App Token</summary>\n\n```python\nprint()\nprint("Get App Token")\nprint(auth.get_app_token())\n```\n\n</details>\n\n<br>\n\n<details>\n<summary>Get User Token</summary>\n\n```python\nprint()\nprint("Get User Code")\nprint(auth.user_code_url)\n\nauth.input_code()\n\n# or\n# auth.code = "USER_CODE"\n\nprint()\nprint("Get User Token")\nprint(auth.get_user_token())\n```\n\n</details>\n\n<br>\n\n<details>\n<summary>Refresh User Token</summary>\n\n```python\nREFRESH_TOKEN = "USER_REFRESH_TOKEN"\n\nprint()\nprint("Refresh User Token")\nprint(auth.update_token(REFRESH_TOKEN))\n```\n\n</details>\n\n\n<br>\n<br>\n\n# 📋 Output Formats\n\n```python\nfrom stalcraft import AppClient\n\nTOKEN = "YOUR_TOKEN"\n\nclient = AppClient(token=TOKEN)\n\nprint()\nprint("Object:")\nprint(client.emission())\n\nclient.json = True\n\n# or\n# client = AppClient(TOKEN, json=True)\n\nprint()\nprint("Json:")\nprint(client.emission())\n```\n\n### Output:\n\n```python\nObject:\nEmission(\n    current_start=None,\n    previous_start=datetime.datetime(2023, 1, 30, 12, 0, 0, tzinfo=datetime.timezone.utc),\n    previous_end=datetime.datetime(2023, 1, 30, 12, 5, 0, tzinfo=datetime.timezone.utc)\n)\n\nJson:\n{\n    \'previousStart\': \'2023-01-30T05:16:52Z\',\n    \'previousEnd\': \'2023-01-30T05:21:52Z\'\n}\n```\n',
    'author': 'onejeuu',
    'author_email': 'bloodtrail@beber1k.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
