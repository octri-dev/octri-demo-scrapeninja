# ScrapeNinja SDK demo with Octri

[![Demo validation](https://github.com/octri-dev/octri-demo-scrapeninja/actions/workflows/demo-validation.yml/badge.svg)](https://github.com/octri-dev/octri-demo-scrapeninja/actions/workflows/demo-validation.yml)

Python and TypeScript SDKs generated with [Octri](https://octri.dev) from ScrapeNinja's OpenAPI specification. This example uses the APIRoad server and its `X-Apiroad-Key` authentication scheme.

The clients provide typed requests and responses, resource namespaces, HTTP error classes, configurable retries, and timeouts. The SDK `src/` files match the original Octri-generated artifacts.

Independent demonstration; not an official ScrapeNinja package.

## Run the example

Requires Python 3.10+ and Node.js 22.12+.

```sh
git clone https://github.com/octri-dev/octri-demo-scrapeninja.git
cd octri-demo-scrapeninja
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm ci --ignore-scripts
.venv/bin/python demos/check-python.py
npm run check:typescript
```

These offline examples exercise the generated client's request serialization, authentication header, and HTML response parsing without needing credentials.

## Call the live API

Set `SCRAPENINJA_API_KEY` to your APIRoad key in your environment, then run:

```sh
.venv/bin/python demos/live-python.py
node demos/live-typescript.cjs
```

Each command makes one real scrape request for `https://example.com` and checks that the SDK returns an HTML body. API usage follows your provider plan. Keys stay in the environment and are not included in the result.

To test the real authentication/error response without a key:

```sh
.venv/bin/python demos/live-python.py --auth-only
node demos/live-typescript.cjs --auth-only
```

[Live test status](evidence/VALIDATION.md): authentication responses checked in both languages; successful authenticated calls await a valid provider key.

## SDK usage

```python
import asyncio
import os
from sdk import ScrapeNinjaAPIRoadUnofficialOctriDemo
from sdk.client import ClientConfig, ClientAuthConfig

async def main():
    config = ClientConfig(
        base_url="https://scrapeninja.apiroad.net",
        auth=ClientAuthConfig(api_key_auth=os.environ["SCRAPENINJA_API_KEY"]),
    )
    try:
        result = await ScrapeNinjaAPIRoadUnofficialOctriDemo(config).scrape.scrape(
            url="https://example.com"
        )
        print(result.body)
    finally:
        await config.aclose()

asyncio.run(main())
```

Install the Python SDK locally from `sdks/apiroad/python`, or build the TypeScript package in `sdks/apiroad/typescript`. These demo distributions are not published to npm or PyPI.

## Checks and source

```sh
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python demos/verify.py
```

The verification command covers SDK tests, formatting, lint, type checks, package builds, and the offline examples. Live calls are separate and never run automatically in CI.

- [Python SDK](sdks/apiroad/python)
- [TypeScript SDK](sdks/apiroad/typescript)
- [OpenAPI configuration](specs/apiroad-demo.json)
- [Original public specification](https://scrapeninja.net/openapi.yaml)
- [Generation provenance](evidence/provenance.json)
