# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_matomo']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.6.0,<4.0.0', 'httpx>=0.24.0,<0.25.0']

setup_kwargs = {
    'name': 'asgi-matomo',
    'version': '0.1.0',
    'description': 'Middleware for tracking ASGI reqeusts with Matomo',
    'long_description': '# asgi-matomo\n[![Packaging status](https://img.shields.io/pypi/v/asgi-matomo?color=%2334D058&label=pypi%20package)](https://pypi.org/project/asgi-matomo)\n[![CI](https://github.com/spraakbanken/asgi-matomo/workflows/CI/badge.svg)](https://github.com/spraakbanken/asgi-matomo/actions?query=workflow%3ACI)\n[![Coverage](https://github.com/spraakbanken/asgi-matomo/workflows/Coverage/badge.svg)](https://github.com/spraakbanken/asgi-matomo/actions?query=workflow%3ACoverage)\n\nTracking requests with Matomo from ASGI apps.\n\n`MatomoMiddleware` adds tracking of all requests to Matomo to ASGI applications (Starlette, FastAPI, Quart, etc.).\n\n**Installation**\n\n```bash\npip install asgi-matomo\n```\n\n## Examples\n\n### Starlette\n\n```python\nfrom starlette.applications import Starlette\nfrom starlette.responses import JSONResponse\nfrom starlette.routing import Route\nfrom starlette.middleware import Middleware\n\nfrom asgi_matomo import MatomoMiddleware\n\nasync def homepage(request):\n    return JSONResponse({"data": "a" * 4000})\n\napp = Starlette(\n  routes=[Route("/", homepage)],\n  middleware=[\n    Middleware(\n      MatomoMiddleware,\n      matomo_url="YOUR MATOMO TRACKING URL",\n      idsite=12345, # your service tracking id\n  )],\n)\n```\n\n### FastAPI\n\n```python\nfrom fastapi import FastAPI\nfrom asgi_matomo import MatomoMiddleware\n\napp = FastAPI()\napp.add_middleware(\n  BrotliMiddleware,\n  matomo_url="YOUR MATOMO TRACKING URL",\n  idsite=12345, # your service tracking id\n)\n\n@app.get("/")\ndef home() -> dict:\n    return {"data": "a" * 4000}\n```\n\n## API Reference\n\n**Overview**\n\n```python\napp.add_middleware(\n  MatomoMiddleware,\n  matomo_url="YOUR MATOMO TRACKING URL",\n  idsite=12345, # your service tracking id\n  access_token="SECRETTOKEN",\n  assume_https=True,\n  minimum_size=400,\n)\n```\n\n**Parameters**:\n\n- **(Required)** `matomo_url`: The URL to make your tracking calls to.\n- **(Required)** `idsite`: The tracking id for your service.\n- _(Optional)_ `access_token`: Access token for Matomo. If this is set `cip` is also tracked. Required for tracking some data.\n- _(Optional)_ `assume_https`: If `True`, set tracked url scheme to `https`, useful when running behind a proxy. Defaults to `True`.\n\n\n**Notes**:\n\n- Currently only some parts [Matomo Tracking HTTP API](https://developer.matomo.org/api-reference/tracking-api) is supported.\n\n## Ideas for further work:\n- _filtering tracked of urls_\n- _custom extraction of tracked data_\n\n\n# Release Notes\n## Latest Changes\n\n## 0.1.0 - 2023-04-28\n\n- Initial release.\n\n',
    'author': 'Kristoffer Andersson',
    'author_email': 'kristoffer.andersson@gu.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
